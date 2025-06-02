from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from .models import EventInfo


def filter_step(image_b64: str) -> bool:
    """
    Determine if this image contains information about an upcoming event.
    
    Args:
        image_b64: Base64 encoded image string
        
    Returns:
        Boolean indicating if the image contains event-related information
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    prompt = "Determine if this image contains information about an upcoming event"
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_b64}"}
            }
        ]
    )
    
    response = llm.invoke([message])
    result = response.content.strip().lower()
    
    # Parse boolean response - look for positive indicators
    positive_indicators = ['yes', 'true', 'contains', 'event']
    negative_indicators = ['no', 'false', 'does not', 'not an event', 'no event']
    
    for indicator in positive_indicators:
        if indicator in result:
            return True
    
    for indicator in negative_indicators:
        if indicator in result:
            return False
            
    # Default to False if unclear
    return False


def summarize_step(image_b64: str, today_date: str) -> str:
    """
    Generate a written summary of the event information in the image.
    
    Args:
        image_b64: Base64 encoded image string
        today_date: Today's date as string for relative time understanding
        
    Returns:
        Text summary of the event
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    prompt = f"""Generate a written summary of the following image that contains information about an event. Be objective and concise, using only information explicitly provided. Emphasize relevant factual elements like time, place, host, etc.

Today's date is: {today_date}"""
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url", 
                "image_url": {"url": f"data:image/png;base64,{image_b64}"}
            }
        ]
    )
    
    response = llm.invoke([message])
    return response.content.strip()


def structure_step(image_b64: str, summary: str) -> EventInfo:
    """
    Extract structured event information from image and summary.
    
    Args:
        image_b64: Base64 encoded image string
        summary: Unstructured text summary from summarize_step
        
    Returns:
        EventInfo object with structured event data
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    parser = PydanticOutputParser(pydantic_object=EventInfo)
    
    prompt = f"""Extract structured information about this event from the image and summary provided.

Summary: {summary}

Please extract the following information if available:
- event_date: the date the event occurs (choose first date if spans multiple days)
- event_starttime: the time the event starts (leave blank if all day)
- event_endtime: the time the event ends (if provided)
- event_venue: the name of the venue hosting the event
- event_location: the address or precise location of the event
- event_description: a short written description using language from the flyer
- event_title: a few-word title for the event (should not be redundant with description)

{parser.get_format_instructions()}"""
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_b64}"}
            }
        ]
    )
    
    response = llm.invoke([message])
    result = parser.parse(response.content)
    
    return result

import base64
import uuid
from datetime import datetime
from pathlib import Path
from typing import List

from .models import EventInfo, ProcessingRun
from .steps import filter_step, summarize_step, structure_step
from .storage import save_processing_run

def process_image(image_path: str, save_run: bool = True) -> EventInfo:
    """
    Process a single image through the complete pipeline.
    
    Args:
        image_path: Path to the image file to process
        save_run: Whether to save the processing run to storage
        
    Returns:
        EventInfo object with extracted event data
        
    Raises:
        Various exceptions if processing fails - let them bubble up for debugging
    """
    # Generate run ID and get current timestamp
    run_id = str(uuid.uuid4())
    timestamp = datetime.now()

    # Load image and convert to base64
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        image_b64 = base64.b64encode(image_data).decode('utf-8')
    
    # Create processing run object to track results
    processing_run = ProcessingRun(
        run_id=run_id,
        input_image_path=image_path,
        timestamp=timestamp,
        config={
            'model': 'gpt-4o',
            'temperature': 0,
        },
        filter_result=None,
        summary_result=None,
        structured_result=None,
    )
    
    structured_result = None
    
    # Step 1: Filter - determine if image contains event info
    filter_result = filter_step(image_b64)
    processing_run.filter_result = filter_result
    
    if filter_result:
        
        # Step 2: Summarize - extract unstructured summary
        summary_result = summarize_step(image_b64, datetime.now().strftime('%Y-%m-%d'))
        processing_run.summary_result = summary_result
        
        # Step 3: Structure - extract structured EventInfo
        structured_result = structure_step(image_b64, summary_result)
        processing_run.structured_result = structured_result
    
    # Save run if requested
    if save_run:
        save_processing_run(processing_run)
    
    # Return final EventInfo result
    return structured_result


def process_directory(dir_path: str) -> List[EventInfo]:
    """
    Process all image files in a directory.
    
    Args:
        dir_path: Path to directory containing image files
        
    Returns:
        List of EventInfo objects, one for each successfully processed image
    """
    results = []
    dir_path_obj = Path(dir_path)
    
    # Define supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png'}
    
    # Find all image files in the directory
    image_files = []
    for file_path in dir_path_obj.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    # Process each image file
    for image_file in image_files:
        try:
            result = process_image(str(image_file), save_run=True)
            results.append(result)
            print(f"Successfully processed: {image_file.name}")
        except Exception as e:
            print(f"Failed to process {image_file.name}: {str(e)}")
            # Continue with next file - don't let one failure stop the batch
            continue
    
    return results

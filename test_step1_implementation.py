import sys
sys.path.insert(0, '/Users/gusrasch/dev/ventii/src')

from ventii.models import EventInfo, ProcessingRun
from datetime import date, time, datetime
import json

# Test EventInfo model
event_info = EventInfo(
    event_date=date(2025, 6, 15),
    event_starttime=time(18, 30),
    event_endtime=time(22, 0),
    event_venue="The Local Theater",
    event_location="123 Main St, Brooklyn, NY",
    event_description="A fantastic evening of live music",
    event_title="Summer Concert Series"
)

print("✓ EventInfo model instantiated successfully")
print("EventInfo JSON:", json.dumps(event_info.model_dump(), default=str, indent=2))

# Test ProcessingRun model
processing_run = ProcessingRun(
    run_id="test-123",
    input_image_path="/path/to/image.jpg",
    filter_result=True,
    summary_result="This is a test summary",
    structured_result=event_info,
    timestamp=datetime.now(),
    config={"model": "gpt-4-vision", "retries": 3}
)

print("\n✓ ProcessingRun model instantiated successfully")
print("ProcessingRun JSON:", json.dumps(processing_run.model_dump(), default=str, indent=2))

# Test with minimal/optional fields
minimal_event = EventInfo()
print("\n✓ EventInfo with all optional fields works")

minimal_run = ProcessingRun(
    run_id="minimal-test",
    input_image_path="/path/to/minimal.jpg",
    timestamp=datetime.now(),
    config={}
)
print("✓ ProcessingRun with minimal required fields works")

print("\n🎉 All model tests passed!")

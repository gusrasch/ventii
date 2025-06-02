from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional


class EventInfo(BaseModel):
    event_date: Optional[date]
    event_starttime: Optional[time]
    event_endtime: Optional[time]
    event_venue: Optional[str]
    event_location: Optional[str]
    event_description: Optional[str]
    event_title: Optional[str]


class ProcessingRun(BaseModel):
    run_id: str
    input_image_path: str
    filter_result: Optional[bool] = None
    summary_result: Optional[str] = None
    structured_result: Optional[EventInfo] = None
    timestamp: datetime
    config: dict

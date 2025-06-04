from .main import process_image, process_directory
from .models import EventInfo

# Export main functions for easy importing
__all__ = ['process_image', 'process_directory', 'EventInfo']


def hello() -> str:
    return "Hello from ventii!"

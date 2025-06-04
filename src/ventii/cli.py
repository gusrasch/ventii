import argparse
import json
import sys
from pathlib import Path
from typing import List

from .main import process_image, process_directory
from .models import EventInfo


def format_eventinfo_as_json(event_info: EventInfo) -> str:
    """Convert EventInfo to JSON string with proper datetime serialization."""
    if event_info is None:
        return json.dumps(None)
    
    # Convert to dict and handle date/time serialization
    data = event_info.model_dump()
    
    # Convert date and time objects to strings for JSON serialization
    if data.get('event_date'):
        data['event_date'] = data['event_date'].isoformat()
    if data.get('event_starttime'):
        data['event_starttime'] = data['event_starttime'].isoformat()
    if data.get('event_endtime'):
        data['event_endtime'] = data['event_endtime'].isoformat()
    
    return json.dumps(data, indent=2)


def format_eventinfo_list_as_json(event_infos: List[EventInfo]) -> str:
    """Convert list of EventInfo objects to JSON string."""
    results = []
    
    for event_info in event_infos:
        if event_info is None:
            results.append(None)
        else:
            data = event_info.model_dump()
            
            # Convert date and time objects to strings for JSON serialization
            if data.get('event_date'):
                data['event_date'] = data['event_date'].isoformat()
            if data.get('event_starttime'):
                data['event_starttime'] = data['event_starttime'].isoformat()
            if data.get('event_endtime'):
                data['event_endtime'] = data['event_endtime'].isoformat()
            
            results.append(data)
    
    return json.dumps(results, indent=2)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Process event flyer images to extract structured information'
    )
    
    # Mutually exclusive group for image vs directory processing
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--image',
        type=str,
        help='Path to a single image file to process'
    )
    input_group.add_argument(
        '--directory',
        type=str,
        help='Path to directory containing image files to process'
    )
    
    # Optional flags
    parser.add_argument(
        '--dev',
        action='store_true',
        help='Development mode flag (currently no-op)'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Skip saving run history'
    )
    
    args = parser.parse_args()
    
    # Determine save_run flag
    save_run = not args.no_save
    
    try:
        if args.image:
            # Process single image
            image_path = Path(args.image)
            
            # Validate image file exists
            if not image_path.exists():
                print(f"Error: Image file not found: {args.image}", file=sys.stderr)
                sys.exit(1)
            
            if not image_path.is_file():
                print(f"Error: Path is not a file: {args.image}", file=sys.stderr)
                sys.exit(1)
            
            # Process the image
            result = process_image(str(image_path), save_run=save_run)
            
            # Print result as JSON
            print(format_eventinfo_as_json(result))
        
        elif args.directory:
            # Process directory of images
            dir_path = Path(args.directory)
            
            # Validate directory exists
            if not dir_path.exists():
                print(f"Error: Directory not found: {args.directory}", file=sys.stderr)
                sys.exit(1)
            
            if not dir_path.is_dir():
                print(f"Error: Path is not a directory: {args.directory}", file=sys.stderr)
                sys.exit(1)
            
            # Process all images in directory
            results = process_directory(str(dir_path))
            
            # Print results as JSON array
            print(format_eventinfo_list_as_json(results))
    
    except Exception as e:
        print(f"Error during processing: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

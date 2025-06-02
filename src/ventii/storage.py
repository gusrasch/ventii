import json
import shutil
from pathlib import Path
from .models import ProcessingRun


def save_processing_run(run: ProcessingRun) -> None:
    """
    Save processing run data and original image for future reference.
    
    Args:
        run: ProcessingRun object containing all processing data
    """
    # Create run history directory structure: run_history/{YYYY-MM-DD}/{run_id}/
    date_str = run.timestamp.strftime('%Y-%m-%d')
    run_dir = Path('run_history') / date_str / run.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    
    # Save run metadata as JSON
    run_data = run.model_dump()
    # Convert datetime to string for JSON serialization
    run_data['timestamp'] = run.timestamp.isoformat()
    
    run_file = run_dir / 'run_data.json'
    with open(run_file, 'w') as f:
        json.dump(run_data, f, indent=2, default=str)
    
    # Copy original image file to run directory for reference
    original_image = Path(run.input_image_path)
    if original_image.exists():
        image_copy = run_dir / f'original_image{original_image.suffix}'
        shutil.copy2(original_image, image_copy)

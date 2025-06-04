# ventii
event flyer processing tool

## Usage

### Prerequisites
```bash
uv pip install -e .
source .env
```

### Process single image
```bash
uv run python -m ventii --image path/to/flyer.jpg
```

### Process directory of images
```bash
uv run python -m ventii --directory path/to/images/
```

### Programmatic use
```python
from ventii import process_image
result = process_image("flyer.jpg")
print(result.event_title)
```

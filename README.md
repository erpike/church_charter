## Code Formatting

This project uses [Black](https://github.com/psf/black), the uncompromising code formatter.

### Installation

Black is included in the project requirements. Install it along with other dependencies:

```bash
pip install -r requirements.txt
```

### Usage

To format a single file:
```bash
black path/to/your/file.py
```

To format all Python files in the project:
```bash
black .
```

To check what files would be formatted without actually changing them:
```bash
black --check .
```

### Configuration

Black configuration is stored in `pyproject.toml`. The current settings:
- Line length: 88 characters
- Target Python version: 3.12
- Includes all Python files (*.py and *.pyi) 
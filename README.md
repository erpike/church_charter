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

### Pre-commit Hooks

This project uses pre-commit hooks to automatically format and check code before each commit. The hooks include:
- Black (code formatting)
- isort (import sorting)
- flake8 (code linting)

#### Setup

1. Install pre-commit:
```bash
pip install pre-commit
```

2. Install the git hooks:
```bash
pre-commit install
```

Now, every time you try to commit, the following will happen automatically:
1. Black will format your Python files
2. isort will sort your imports
3. flake8 will check your code for style issues

If any of these checks fail, the commit will be blocked until you fix the issues.

#### Manual Run

To manually run the pre-commit hooks on all files:
```bash
pre-commit run --all-files
```

To run a specific hook:
```bash
pre-commit run black --all-files
``` 
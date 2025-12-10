# Contributing to Custom CSV Reader and Writer

## Welcome!

Thank you for your interest in contributing to this educational project. This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on learning and improvement
- Provide constructive feedback

## How to Contribute

### 1. Fork the Repository

```bash
git clone https://github.com/yourusername/custom-csv-reader-writer.git
cd custom-csv-reader-writer
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Keep changes focused and minimal

### 4. Test Your Changes

```bash
python test_csv.py
```

### 5. Commit and Push

```bash
git add .
git commit -m "Descriptive commit message"
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

Open a PR on GitHub with a clear description of changes.

## Development Setup

### Requirements

- Python 3.7+
- No external dependencies

### Optional Development Tools

```bash
pip install pytest black flake8 mypy
```

### Code Style

```bash
# Format code
black custom_csv.py benchmark.py test_csv.py

# Check style
flake8 custom_csv.py benchmark.py test_csv.py

# Type checking
mypy custom_csv.py
```

## Areas for Contribution

### 1. Bug Fixes
- Report bugs with clear examples
- Submit PRs with fixes and tests

### 2. Performance Improvements
- Profile code to identify bottlenecks
- Document performance changes
- Include benchmark comparisons

### 3. Feature Additions
- Dialect support (tab-delimited, semicolon, etc.)
- Skip empty lines option
- Comment row handling
- Type conversion support
- Better error handling with custom exceptions

### 4. Documentation
- Improve existing documentation
- Add tutorials and examples
- Clarify complex sections
- Add docstring improvements

### 5. Testing
- Add edge case tests
- Improve test coverage
- Add performance benchmarks

## Testing Guidelines

### Running Tests

```bash
python test_csv.py
```

### Writing New Tests

```python
def test_your_feature():
    """Test description."""
    # Setup
    data = [[...]]
    
    # Execute
    result = your_function(data)
    
    # Assert
    assert result == expected
    print("✓ test_your_feature passed")
```

## Documentation Standards

### Module-Level Docstrings

```python
"""Brief description.

Detailed explanation if needed.
"""
```

### Function Docstrings

```python
def function(param1, param2):
    """Brief description.
    
    Parameters
    ----------
    param1 : type
        Description
    param2 : type
        Description
    
    Returns
    -------
    type
        Description
    """
```

## Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Be descriptive and specific
- Reference issues when relevant: "Fixes #123"
- Keep first line under 50 characters

## Review Process

1. Maintainers review your PR
2. Address feedback and update PR
3. Ensure all tests pass
4. Merge once approved

## Questions?

- Open an issue for discussion
- Ask in PR comments
- Reference DESIGN.md for architecture details

## Thank You!

Your contributions help improve this educational resource for everyone!

# Contributing to YouTube Audio Telegram Bot

First off, thank you for considering contributing to this project! It's people like you that make this bot better for everyone. Following these guidelines helps communicate that you respect the time of the developers managing and developing this open source project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How Can I Contribute?](#how-can-i-contribute)
4. [Development Setup](#development-setup)
5. [Style Guidelines](#style-guidelines)
6. [Commit Messages](#commit-messages)
7. [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

Before you begin:

- Have you read the [README](README.md)?
- Check if your issue/idea already exists in [Issues](https://github.com/d-dziublenko/telegram-audio-bot/issues)
- For major changes, open an issue first to discuss what you would like to change

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

**How to submit a bug report:**

1. Use a clear and descriptive title
2. Describe the exact steps to reproduce the problem
3. Provide specific examples to demonstrate the steps
4. Include Python version, OS details, and error messages
5. Explain what you expected to happen instead

**Example bug report:**

```markdown
Title: Bot crashes when URL contains special Unicode characters

Steps to reproduce:

1. Send the bot a YouTube URL with Unicode: https://youtube.com/watch?v=xxx&title=测试
2. Bot responds with "Processing your video..."
3. Bot crashes with UnicodeEncodeError

Expected behavior:
Bot should handle Unicode characters in URLs gracefully

Environment:

- Python 3.9.2
- Ubuntu 20.04
- Error: UnicodeEncodeError: 'ascii' codec can't encode character
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

1. Use a clear and descriptive title
2. Provide a detailed description of the proposed enhancement
3. Explain why this enhancement would be useful to most users
4. List any alternative solutions you've considered

### Your First Code Contribution

Unsure where to begin? Look for these tags in issues:

- `good first issue` - Simple issues good for beginners
- `help wanted` - Issues where we need community help
- `enhancement` - New features you could implement

## Development Setup

1. Fork the repository and clone your fork:

   ```bash
   git clone https://github.com/d-dziublenko/telegram-audio-bot.git
   cd telegram-audio-bot
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

3. Create a branch for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. Make your changes and test thoroughly:

   ```bash
   # Run the bot to test your changes
   python bot.py

   # If tests exist, run them
   pytest
   ```

5. Commit your changes (see commit message guidelines below)

6. Push to your fork and submit a pull request

## Style Guidelines

### Python Style Guide

We follow PEP 8 with a few modifications:

- Line length: 100 characters maximum (not 79)
- Use meaningful variable names (not just single letters except for loop counters)
- Add type hints where they improve clarity
- All functions must have docstrings

**Example of good code style:**

```python
def download_audio(url: str, output_dir: Path) -> Path:
    """
    Download audio from YouTube video.

    Args:
        url: YouTube video URL
        output_dir: Directory to save the audio file

    Returns:
        Path to the downloaded audio file

    Raises:
        ValueError: If URL is invalid
        ConnectionError: If download fails
    """
    # Implementation here
```

### Documentation Style

- Use clear, simple English
- Include code examples where helpful
- Keep README sections concise but complete
- Update documentation when changing functionality

## Commit Messages

We follow the Conventional Commits specification:

**Format:** `type(scope): description`

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc)
- `refactor`: Code changes that neither fix bugs nor add features
- `test`: Adding or fixing tests
- `chore`: Changes to build process or auxiliary tools

**Examples:**

```
feat(bot): add support for playlist downloads
fix(download): handle URLs with special characters
docs(readme): update installation instructions
style(bot): format code with black
refactor(audio): extract download logic to separate function
test(sanitize): add tests for filename sanitization
chore(deps): update pytube to version 15.0.0
```

**Commit message guidelines:**

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- First line should be under 72 characters
- Reference issues and pull requests when relevant

## Pull Request Process

1. **Before submitting:**

   - Update the README.md with details of changes if needed
   - Ensure your code follows the style guidelines
   - Add any necessary tests
   - Update documentation for any changed functionality
   - Make sure all tests pass

2. **PR description should include:**

   - What changes were made and why
   - Any breaking changes
   - Issues this PR closes (use "Closes #123" syntax)
   - Screenshots for UI changes (if applicable)

3. **After submitting:**
   - Be responsive to code review feedback
   - Make requested changes in new commits (don't force-push)
   - Once approved, we'll merge your PR!

### Pull Request Template

```markdown
## Description

Brief description of what this PR does

## Type of change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing

- [ ] I have tested this locally
- [ ] I have added tests that prove my fix/feature works
- [ ] All existing tests pass

## Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation accordingly
- [ ] My changes generate no new warnings

## Related Issues

Closes #(issue number)

## Screenshots (if applicable)
```

## Recognition

Contributors who submit accepted pull requests will be added to our Contributors section in the README. We appreciate every contribution, no matter how small!

## Questions?

Feel free to open an issue with the tag `question` if you need clarification on anything. We're here to help!

## Thank You!

Your contributions make open source amazing. We're excited to see what you'll add to this project!

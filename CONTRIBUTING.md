# Contributing to Get Started with Edge AI

Thank you for your interest in contributing to this project! We welcome contributions from the community to help make Edge AI more accessible to everyone.

## How to Contribute

### Reporting Issues

Before creating an issue, please:

1. Check if the issue already exists in our [issue tracker](https://github.com/Arm-Examples/Get-Started-with-Edge-AI/issues)
2. Make sure you're using the latest version of the code
3. Test your issue with a clean environment

When creating an issue, please include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Your operating system and Python version
- Any relevant error messages or logs

### Suggesting Enhancements

We'd love to hear your ideas for new examples or improvements! Please:

1. Check existing issues and discussions first
2. Create an issue with the "enhancement" label
3. Describe your idea clearly with use cases and benefits
4. Consider if it fits the project's goal of accessible Edge AI examples

### Contributing Code

#### Development Setup

1. Fork the repository
2. Clone your fork:

   ```bash
   git clone https://github.com/YOUR_USERNAME/Get-Started-with-Edge-AI.git
   cd Get-Started-with-Edge-AI
   ```

3. Create a virtual environment:

   ```bash
   python -m venv edge-ai-env
   source edge-ai-env/bin/activate  # On Windows: edge-ai-env\Scripts\activate
   ```

4. Install dependencies for the example you're working on:

   ```bash
   cd example_folder
   pip install -r requirements.txt
   ```

#### Making Changes

1. Create a new branch for your feature/fix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Test your changes thoroughly
4. Add or update documentation as needed
5. Commit your changes with clear commit messages:

   ```bash
   git commit -m "Add: brief description of your change"
   ```

#### Pull Request Process

1. Push your branch to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a pull request from your fork to the main repository
3. Fill out the pull request template completely
4. Link any related issues
5. Wait for review and address any feedback

### Code Style and Standards

- Follow [ruff](https://github.com/astral-sh/ruff) for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Include docstrings for functions and classes
- Keep examples simple and beginner-friendly
- Test your code on different platforms when possible

### Adding New Examples

When adding new Edge AI examples:

1. Create a new folder with a descriptive name
2. Include a detailed README.md with:
   - Clear description of what the example demonstrates
   - Requirements and setup instructions
   - Expected output or behavior
   - Performance considerations
3. Add a requirements.txt file
4. Keep dependencies minimal and well-justified
5. Test on different hardware configurations
6. Update the main README.md to reference your example

### Documentation

- Keep documentation clear and beginner-friendly
- Include screenshots or GIFs where helpful
- Test all code examples and instructions
- Use consistent formatting and style

### Community Guidelines

- Be respectful and inclusive
- Help newcomers to Edge AI
- Focus on educational value
- Share knowledge and learn from others

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the "question" label
- Start a discussion in the repository
- Reach out to the maintainers

Thank you for helping make Edge AI more accessible!

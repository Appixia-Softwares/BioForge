# Contributing to BioForge

First off, thank you for considering contributing to BioForge! It's people like you that make BioForge such a great tool for the synthetic biology community.

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to [conduct@appixia.com](mailto:conduct@appixia.com).

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for BioForge. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

- **Use the GitHub issue tracker** — Check if the bug has already been reported by searching on GitHub under [Issues](https://github.com/Appixia-Softwares/BioForge/issues).
- **Use the bug report template** — When you create a new issue, you'll see a template for bug reports. Please fill it out completely.
- **Include detailed information** — Include as many details as possible: which version you're using, what environment (browser, OS), steps to reproduce, expected behavior, and actual behavior.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for BioForge, including completely new features and minor improvements to existing functionality.

- **Use the GitHub issue tracker** — Check if the enhancement has already been suggested by searching on GitHub under [Issues](https://github.com/Appixia-Softwares/BioForge/issues).
- **Use the feature request template** — When you create a new issue, you'll see a template for feature requests. Please fill it out completely.
- **Describe the enhancement in detail** — Provide a clear description of what you want to happen, why it would be beneficial, and how it should work.

### Your First Code Contribution

Unsure where to begin contributing to BioForge? You can start by looking through these `beginner-friendly` and `help-wanted` issues:

- [Beginner-friendly issues](https://github.com/Appixia-Softwares/BioForge/labels/beginner-friendly) - issues which should only require a few lines of code, and a test or two.
- [Help wanted issues](https://github.com/Appixia-Softwares/BioForge/labels/help-wanted) - issues which should be a bit more involved than `beginner-friendly` issues.

### Pull Requests

- Fill in the required template
- Follow the [style guides](#style-guides)
- Include appropriate tests
- Update documentation as needed
- Make sure all tests pass
- Include screenshots and animated GIFs in your pull request whenever possible

## Style Guides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - 🐎 `:racehorse:` when improving performance
  - 🔒 `:lock:` when dealing with security
  - 📝 `:memo:` when writing docs
  - 🐛 `:bug:` when fixing a bug
  - 🔥 `:fire:` when removing code or files
  - 💚 `:green_heart:` when fixing the CI build
  - ✅ `:white_check_mark:` when adding tests
  - ⬆️ `:arrow_up:` when upgrading dependencies
  - ⬇️ `:arrow_down:` when downgrading dependencies
  - 👕 `:shirt:` when removing linter warnings

### JavaScript/TypeScript Style Guide

- We use [ESLint](https://eslint.org/) and [Prettier](https://prettier.io/) for JavaScript/TypeScript code
- Follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use TypeScript for type safety
- Use functional components and hooks for React

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/en/stable/) for code formatting
- Use type hints
- Write docstrings for all functions, classes, and modules

### Documentation Style Guide

- Use [Markdown](https://daringfireball.net/projects/markdown/) for documentation
- Reference functions, classes, and modules in backticks: `like_this`
- Use code blocks with appropriate language syntax highlighting
- Include examples and screenshots where appropriate

## Development Setup

### Frontend

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

### Backend

\`\`\`bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

### AI Service

\`\`\`bash
cd ai-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
\`\`\`

### Safety Service

\`\`\`bash
cd safety-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
\`\`\`

### Simulation Service

\`\`\`bash
cd simulation-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8003
\`\`\`

### Data Pipelines

\`\`\`bash
cd data-pipelines
pip install -r requirements.txt
uvicorn main:app --reload --port 8004
\`\`\`

### Blockchain

\`\`\`bash
cd blockchain
npm install
npx hardhat compile
\`\`\`

## Testing

- Frontend: `cd frontend && npm test`
- Backend: `cd backend && pytest`
- AI Service: `cd ai-service && pytest`
- Safety Service: `cd safety-service && pytest`
- Simulation Service: `cd simulation-service && pytest`
- Data Pipelines: `cd data-pipelines && pytest`
- Blockchain: `cd blockchain && npx hardhat test`

## Additional Resources

- [Project Roadmap](docs/roadmap.md)
- [Architecture Overview](ARCHITECTURE.md)
- [API Documentation](docs/api-docs.md)
- [Development Guide](DEVELOPMENT.md)
- [Setup Guide](SETUP.md)

Thank you for your contributions!

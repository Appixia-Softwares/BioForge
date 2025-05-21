# BioForge Development Guide

This guide provides information for developers who want to contribute to the BioForge platform.

## Development Environment

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js](https://nodejs.org/) (v18 or later)
- [Python](https://www.python.org/) (v3.9 or later)
- [Git](https://git-scm.com/)
- [Visual Studio Code](https://code.visualstudio.com/) (recommended) or your preferred IDE

### Recommended Extensions for VS Code

- ESLint
- Prettier
- Python
- Docker
- Tailwind CSS IntelliSense
- Solidity
- GitLens
- Error Lens
- Import Cost
- Path Intellisense

### Environment Setup

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/Appixia-Softwares/BioForge.git
   cd BioForge
   \`\`\`

2. Set up environment variables:
   - Copy the `.env.example` file to `.env`:
     \`\`\`bash
     cp .env.example .env
     \`\`\`
   - Fill in the environment variables in the `.env` file with your configuration

3. Start the development environment:
   \`\`\`bash
   docker-compose -f docker-compose.dev.yml up
   \`\`\`

## Project Structure

\`\`\`
BioForge/
├── .github/                # GitHub workflows and templates
├── app/                    # Main application
├── backend/                # API Gateway (FastAPI)
│   ├── main.py             # Main application entry point
│   ├── models/             # Data models
│   ├── services/           # Service integrations
│   └── utils/              # Utility functions
├── frontend/               # Frontend (Next.js)
│   ├── app/                # Next.js app directory
│   ├── components/         # React components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utility functions
│   └── public/             # Static assets
├── ai-service/             # AI Service (FastAPI, PyTorch)
│   ├── main.py             # Main application entry point
│   └── models/             # AI models
├── safety-service/         # Safety Service (FastAPI)
│   └── main.py             # Main application entry point
├── simulation-service/     # Simulation Service (FastAPI)
│   └── main.py             # Main application entry point
├── data-pipelines/         # Data Pipelines (FastAPI)
│   └── main.py             # Main application entry point
├── blockchain/             # Blockchain (Solidity, Hardhat)
│   ├── contracts/          # Smart contracts
│   ├── scripts/            # Deployment scripts
│   └── test/               # Contract tests
└── docs/                   # Documentation
\`\`\`

## Development Workflow

### Git Workflow

We follow the [GitHub Flow](https://guides.github.com/introduction/flow/) model:

1. Create a branch from `main` for your feature or bugfix
2. Make your changes
3. Create a pull request to merge your branch into `main`
4. Request a review from a team member
5. Once approved, merge your pull request

### Branch Naming Convention

- Feature branches: `feature/feature-name`
- Bugfix branches: `bugfix/bug-name`
- Hotfix branches: `hotfix/issue-name`
- Release branches: `release/version-number`

### Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

\`\`\`
<type>(<scope>): <description>

[optional body]

[optional footer]
\`\`\`

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: Code changes that neither fix a bug nor add a feature
- `perf`: Performance improvements
- `test`: Adding or fixing tests
- `chore`: Changes to the build process or auxiliary tools

Example:
\`\`\`
feat(designer): add drag-and-drop functionality for DNA parts

Implemented drag-and-drop functionality for the DNA Designer component
using React DnD. This allows users to drag parts from the palette and
drop them onto the canvas.

Closes #123
\`\`\`

### Pull Request Process

1. Ensure your code follows the project's coding standards
2. Update the documentation if necessary
3. Add tests for your changes
4. Ensure all tests pass
5. Request a review from a team member
6. Address any feedback from the review
7. Once approved, merge your pull request

## Coding Standards

### General

- Use consistent indentation (2 spaces for JavaScript/TypeScript, 4 spaces for Python)
- Keep lines under 100 characters
- Use meaningful variable and function names
- Write comments for complex logic
- Follow the DRY (Don't Repeat Yourself) principle

### JavaScript/TypeScript

- Follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use TypeScript for type safety
- Use ESLint and Prettier for code formatting
- Use functional components and hooks for React
- Use async/await for asynchronous code

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints
- Use Black for code formatting
- Write docstrings for all functions, classes, and modules

### Solidity

- Follow the [Solidity Style Guide](https://docs.soliditylang.org/en/latest/style-guide.html)
- Use the latest stable Solidity version
- Follow security best practices
- Use NatSpec comments for documentation

## Testing

### Frontend

We use Jest and React Testing Library for frontend testing:

\`\`\`bash
cd frontend
npm test
\`\`\`

### Backend

We use pytest for backend testing:

\`\`\`bash
cd backend
pytest
\`\`\`

### AI Service

\`\`\`bash
cd ai-service
pytest
\`\`\`

### Safety Service

\`\`\`bash
cd safety-service
pytest
\`\`\`

### Simulation Service

\`\`\`bash
cd simulation-service
pytest
\`\`\`

### Data Pipelines

\`\`\`bash
cd data-pipelines
pytest
\`\`\`

### Blockchain

We use Hardhat for blockchain testing:

\`\`\`bash
cd blockchain
npx hardhat test
\`\`\`

## Debugging

### Frontend

- Use the React Developer Tools browser extension
- Use the console.log() method for debugging
- Use the debugger statement to pause execution

### Backend

- Use the built-in debugger in your IDE
- Use logging with different log levels
- Use pdb for interactive debugging

### Blockchain

- Use Hardhat's console.log for Solidity debugging
- Use Hardhat's network forking for testing with mainnet state

## Documentation

- Update the documentation when you make changes
- Use JSDoc for JavaScript/TypeScript
- Use docstrings for Python
- Follow the [Documentation Style Guide](docs/style-guide.md)
- Keep the [API Documentation](docs/api-docs.md) up to date
- Update the [Architecture Documentation](ARCHITECTURE.md) for significant changes
- Document all environment variables in `.env.example`

## Troubleshooting

### Common Issues

1. **Docker Issues**
   - Ensure Docker daemon is running
   - Check port conflicts
   - Clear Docker cache if needed: \`docker system prune -a\`

2. **Node.js Issues**
   - Clear npm cache: \`npm cache clean --force\`
   - Delete node_modules and reinstall: \`rm -rf node_modules && npm install\`

3. **Python Issues**
   - Create a new virtual environment
   - Update pip: \`python -m pip install --upgrade pip\`
   - Install requirements: \`pip install -r requirements.txt\`

4. **Blockchain Issues**
   - Ensure MetaMask is installed and configured
   - Check network connectivity
   - Verify contract deployment

### Getting Help

- Check the [GitHub Issues](https://github.com/Appixia-Softwares/BioForge/issues)
- Join our [Discord Community](https://discord.gg/appixia)
- Contact the development team at [dev@appixia.com](mailto:dev@appixia.com)

## Continuous Integration

We use GitHub Actions for continuous integration:

- Linting
- Testing
- Building
- Deployment

The CI pipeline is defined in `.github/workflows/ci.yml`.

## Deployment

### Development

\`\`
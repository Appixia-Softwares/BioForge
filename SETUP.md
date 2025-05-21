# BioForge Setup Guide

This guide will help you set up and run the BioForge platform locally for development.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js](https://nodejs.org/) (v18 or later)
- [Python](https://www.python.org/) (v3.9 or later)
- [Git](https://git-scm.com/)

## Environment Setup

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/bioforge/bioforge.git
   cd bioforge
   \`\`\`

2. Create a Firebase project:
   - Go to the [Firebase Console](https://console.firebase.google.com/)
   - Create a new project
   - Add a web app to your project
   - Enable Authentication (Email/Password)
   - Create a Firestore database
   - Generate a service account key (Project Settings > Service accounts > Generate new private key)
   - Save the key as `firebase-service-account.json` in the root directory

3. Set up environment variables:
   - Copy the `.env.example` file to `.env`:
     \`\`\`bash
     cp .env.example .env
     \`\`\`
   - Fill in the environment variables in the `.env` file:
     - Firebase configuration (from your Firebase project settings)
     - Blockchain configuration (if you're using the blockchain features)

## Running with Docker Compose

For a full development environment with all services:

\`\`\`bash
# Start the development environment
docker-compose -f docker-compose.dev.yml up

# Access the services:
# - Frontend: http://localhost:3000
# - API Gateway: http://localhost:8000
# - API Documentation: http://localhost:8000/docs
\`\`\`

## Running Individual Components

### Frontend

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

The frontend will be available at http://localhost:3000.

### Backend (API Gateway)

\`\`\`bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

The API Gateway will be available at http://localhost:8000.

### AI Service

\`\`\`bash
cd ai-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
\`\`\`

The AI Service will be available at http://localhost:8001.

### Safety Service

\`\`\`bash
cd safety-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
\`\`\`

The Safety Service will be available at http://localhost:8002.

### Simulation Service

\`\`\`bash
cd simulation-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8003
\`\`\`

The Simulation Service will be available at http://localhost:8003.

### Data Pipelines

\`\`\`bash
cd data-pipelines
pip install -r requirements.txt
uvicorn main:app --reload --port 8004
\`\`\`

The Data Pipelines service will be available at http://localhost:8004.

### Blockchain (Smart Contracts)

\`\`\`bash
cd blockchain
npm install
npx hardhat compile
\`\`\`

To deploy to a test network:

\`\`\`bash
npx hardhat run scripts/deploy.js --network mumbai
\`\`\`

## Development Workflow

1. Make changes to the code
2. Run tests:
   - Frontend: `cd frontend && npm test`
   - Backend: `cd backend && pytest`
   - AI Service: `cd ai-service && pytest`
   - Safety Service: `cd safety-service && pytest`
   - Simulation Service: `cd simulation-service && pytest`
   - Data Pipelines: `cd data-pipelines && pytest`
   - Blockchain: `cd blockchain && npx hardhat test`
3. Commit your changes
4. Create a pull request

## Troubleshooting

### Common Issues

1. **Docker Compose Network Issues**
   - If services can't communicate with each other, check the network configuration in `docker-compose.yml`
   - Ensure all services are on the same network

2. **Firebase Authentication Issues**
   - Verify that your Firebase configuration is correct
   - Check that Authentication is enabled in the Firebase Console

3. **AI Service GPU Issues**
   - If you're using a GPU, ensure CUDA is properly installed
   - Check that the CUDA version is compatible with the PyTorch version

4. **Blockchain Connection Issues**
   - Verify that your RPC URL and private key are correct
   - Ensure you have enough test ETH/MATIC for transactions

### Getting Help

If you encounter any issues not covered here, please:
- Check the [documentation](docs/)
- Open an issue on GitHub
- Reach out to the community on Discord

## Next Steps

Once you have the platform running, you can:
1. Create a user account
2. Design your first synthetic biology circuit
3. Run simulations and safety checks
4. Mint an IP-NFT for your design

For more detailed instructions, see the [User Guide](docs/user-guide.md).

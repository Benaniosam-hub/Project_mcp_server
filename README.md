# Project_mcp_server_Claude

An automated CI/CD Flask REST API deployment pipeline to AWS ECS using GitHub Actions.

## Overview

This repository demonstrates a production-ready deployment workflow for a Flask-based REST API to Amazon Web Services (AWS) using GitHub Actions. It includes:

- ✅ REST API for employee/student management built with Flask
- ✅ PostgreSQL integration (AWS RDS) for persistent storage
- ✅ Docker containerization for consistent environments
- ✅ Automated CI/CD pipeline using GitHub Actions
- ✅ Deployment to AWS ECS with automatic image updates

## Tech Stack

- Language: Python 3.13+ (repo shows Python)
- Framework: FastMCP / Flask (repo contains an MCP server; adapt as needed)
- Database: PostgreSQL (AWS RDS)
- Container: Docker
- Container Registry: AWS ECR Public
- Orchestration: AWS ECS
- CI/CD: GitHub Actions
- Cloud Region (example): ap-south-2 (Mumbai)

## Repository structure

Project_mcp_server_Claude/
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions deployment workflow (if present)
├── main.py / server.py             # MCP / Flask server entrypoint
├── Dockerfile                      # Docker image configuration (if present)
├── pyproject.toml                  # Python project metadata & dependencies
├── requirements.txt                # Python dependencies (if present)
├── Output_images/                  # Documentation & screenshots
└── README.md                       # This file

## API / Tools (example)

Depending on the repository implementation, the server exposes one or more of the following:

- say_hello or GET /hello
  Response: {"sharlin": "Hello benanio"}

- get_status
  Response: "Server is running"

- run_query(query: str) / GET /students / POST /students
  - run_query executes SQL against PostgreSQL with a basic blacklist of destructive statements
  - GET /students returns a list of students
  - POST /students adds a student and returns a success message

Adjust these to match the functions/endpoints in the code (main.py / server.py / app.py).

## Architecture (diagram)

Below is an architecture diagram that illustrates how code flows from your GitHub repository through GitHub Actions into AWS ECR and AWS ECS, with the application connecting to RDS (PostgreSQL).

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          GITHUB REPOSITORY                             │
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────────┐            │
│  │   server.py  │    │ Dockerfile   │    │ .github/workflows│            │
│  │ (MCP/Flask)  │    │ (Python 3.x) │    │   └─ deploy.yml  │            │
│  └──────────────┘    └──────────────┘    └─────────────────┘            │
│                                                                         │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                        Git Push to main branch
                                 │
                                 ▼
         ┌───────────────────────────────────────────────┐
         │      GITHUB ACTIONS CI/CD PIPELINE            │
         │                                               │
         │  ┌─────────────────────────────────────────┐  │
         │  │ Step 1: Checkout Code                   │  │
         │  └─────────────────────────────────────────┘  │
         │                    │                           │
         │                    ▼                           │
         │  ┌─────────────────────────────────────────┐  │
         │  │ Step 2: Configure AWS Credentials      │  │
         │  │ (IAM Access Key + Secret Key)          │  │
         │  └─────────────────────────────────────────┘  │
         │                    │                           │
         │                    ▼                           │
         │  ┌─────────────────────────────────────────┐  │
         │  │ Step 3: Login to ECR Public             │  │
         │  │ (AWS ECR Authentication)                │  │
         │  └─────────────────────────────────────────┘  │
         │                    │                           │
         │                    ▼                           │
         │  ┌─────────────────────────────────────────┐  │
         │  │ Step 4: Build Docker Image              │  │
         │  │ docker build -t app:$IMAGE_TAG .       │  │
         │  └─────────────────────────────────────────┘  │
         │                    │                           │
         │                    ▼                           │
         │  ┌─────────────────────────────────────────┐  │
         │  │ Step 5: Tag & Push to ECR Public        │  │
         │  │ public.ecr.aws/<alias>/app:TAG         │  │
         │  └─────────────────────────────────────────┘  │
         │                    │                           │
         └────────────────────┼───────────────────────────┘
                              │
                              ▼
         ┌───────────────────────────────────────────────┐
         │   AWS ECR PUBLIC (Elastic Container Registry) │
         │                                               │
         │  ┌─────────────────────────────────────────┐  │
         │  │  app:commit-sha                        │  │
         │  │  (Docker Image Stored)                  │  │
         │  └─────────────────────────────────────────┘  │
         │                                               │
         └────────────────────┬───────────────────────────┘
                              │
                              ▼
         ┌───────────────────────────────────────────────┐
         │      GITHUB ACTIONS DEPLOYMENT STAGE          │
         │                                               │
         │  ┌─────────────────────────────────────────┐  │
         │  │ Step 6: Download ECS Task Definition    │  │
         │  │ (Current running task config)           │  │
         │  └─────────────────────────────────────────┘  │
         │                    │                           │
         │                    ▼                           │
         │  ┌─────────────────────────────────────────┐  │
         │  │ Step 7: Render New Task Definition      │  │
         │  │ (Update with new image URI)             │  │
         │  └─────────────────────────────────────────┘  │
         │                    │                           │
         │                    ▼                           │
         │  ┌─────────────────────────────────────────┐  │
         │  │ Step 8: Deploy to ECS Service           │  │
         │  │ (Update app-task-service)               │  │
         │  └─────────────────────────────────────────┘  │
         │                                               │
         └────────────────────┬───────────────────────────┘
                              │
                              ▼
         ┌───────────────────────────────────────────────┐
         │        AWS ECS CLUSTER (ap-south-2)           │
         │                                               │
         │  Cluster: app-cluster                         │
         │                                               │
         │  ┌──────────────────────────────────────────┐ │
         │  │  ECS Service: app-task-service            │ │
         │  │  ┌────────────────────────────────────┐  │ │
         │  │  │ Container: app-container            │  │ │
         │  │  │  ┌────────────────────────────────┐ │  │
         │  │  │  │ Application (Flask / MCP)      │ │  │
         │  │  │  │ Port: 5000                      │ │  │
         │  │  │  └────────────────────────────────┘ │  │
         │  │  └────────────────────────────────────┘  │ │
         │  └──────────────────────────────────────────┘ │
         │             │                                 │
         └─────────────┼─────────────────────────────────┘
                       │
                       ▼ (Network call)
         ┌─────────────────────────────────────────────────┐
         │    AWS RDS (Relational Database Service)        │
         │    PostgreSQL Database (ap-south-2)             │
         │                                                 │
         │  ┌──────────────────────────────────────────┐   │
         │  │ Database: postgres                       │   │
         │  │ Tables: students                         │   │
         │  └──────────────────────────────────────────┘   │
         └─────────────────────────────────────────────────┘
```

## Getting started (local)

Prerequisites:
- Python 3.13+
- Docker
- (Optional) AWS account and configured resources for deployment

Clone and run locally:
```bash
git clone https://github.com/Benaniosam-hub/Project_mcp_server_Claude.git
cd Project_mcp_server_Claude
# If requirements.txt exists
pip install -r requirements.txt

# Set environment variables (example)
export PG_HOST=your-postgres-host
export PG_DATABASE=postgres
export PG_USER=postgres
export PG_PASSWORD=your-password

# Run the server (adjust the entrypoint file: main.py / server.py / app.py)
python server.py
# API available at http://localhost:5000
```

Test endpoints locally:
```bash
curl http://localhost:5000/hello
curl http://localhost:5000/students
curl -X POST http://localhost:5000/students -H "Content-Type: application/json" -d '{"name":"Test Student","age":20}'
```

## Docker (local)

Build and run:
```bash
docker build -t app:latest .
docker run -p 5000:5000 \
  -e PG_HOST=your-postgres-host \
  -e PG_DATABASE=postgres \
  -e PG_USER=postgres \
  -e PG_PASSWORD=your-password \
  app:latest
```

## Deployment with GitHub Actions (automated)

This repository may include a workflow (.github/workflows/deploy.yml) that:

1. Triggers on push to the main branch
2. Checks out the code
3. Configures AWS credentials from repository Secrets
4. Builds and tags a Docker image
5. Pushes the image to AWS ECR Public
6. Downloads the current ECS task definition, injects the new image URI, registers the task, and updates the ECS service

Recommended GitHub Secrets to configure:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

Example AWS resources used by the workflow (update names to match your AWS account):
- ECS Cluster: flask-api-cluster
- ECS Service: flask-api-task-service
- Task Definition family: flask-api-task
- ECR Repository: flask-api (public alias placeholder)
- Region: ap-south-2

## Environment variables

| Variable    | Default (example)                                           | Description                   |
|-------------|-------------------------------------------------------------|-------------------------------|
| PG_HOST     | localhost / your DB host                                     | PostgreSQL host               |
| PG_DATABASE | postgres                                                    | Database name                 |
| PG_USER     | postgres                                                    | Database user                 |
| PG_PASSWORD | (set securely)                                              | Database password             |

Make sure to change defaults before production deployment.

## Security considerations

- Do NOT hardcode secrets in source files. Use environment variables or a secrets manager (AWS Secrets Manager).
- Use least-privilege IAM policies for GitHub Actions/AWS roles.
- Place RDS in a private subnet and restrict access via security groups.
- Enable TLS/HTTPS for external traffic (ALB, API Gateway, or reverse proxy).
- Rotate credentials and monitor logs (CloudWatch).

## Troubleshooting

- Database connection errors: check DB endpoint, credentials, and security group ingress from ECS.
- ECS deployment failures: review CloudWatch logs and ECS events; ensure task role and service role permissions are correct.
- GitHub Actions failures: inspect workflow run logs in Actions tab and validate Secrets.

## Future enhancements

- Add auth (JWT / OAuth)
- Input validation and improved error handling
- Database migrations (Alembic)
- Unit & integration tests
- Structured logging and monitoring
- API docs (OpenAPI / Swagger)
- CI tests before deployment
- Health checks and auto-scaling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

## License

If you plan to open-source, add a LICENSE file (MIT, Apache-2.0, etc.).

## Author

Benaniosam — https://github.com/Benaniosam-hub

## Support

Open an issue on the GitHub repository: https://github.com/Benaniosam-hub/Project_mcp_server_Claude/issues

---

**Last Updated:** 2026-06-27  
**Version:** 1.1.0

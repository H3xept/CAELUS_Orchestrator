# CAELUS_Orchestrator
The API that deals with spawning and managing digital twin instances.

# Install
To install the orchestrator:
1. Create a `.env` file in the root directory of the project with contents: 

```
DOCKER_PAT=<DOCKER_PAT>
DOCKER_USER=<username for docker registry>
DOCKER_EMAIL=<email for docker registry>
DOCKER_REGISTRY=ghcr.io
APP_SECRET=<an appliction secret>
DEFAULT_ADMIN_PASSWORD=<a default admin password>
DELETE_CONTAINERS=True
MAX_CONCURRENT_PROCESSES=8
```

2. Run `bash start.sh`

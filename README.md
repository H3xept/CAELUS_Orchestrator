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

## Job error types
`UNDEFINED_ERROR = 1`
Description: An undefined error occurred.
Action: Unknown

`JSON_READ_EC = 2`
Description: Error while reading the json file
Action: Fix the json file

`MISSION_UPLOAD_FAIL = 3`
Description: Error while uploading the mission file
Action: Try again, the server may be overloaded

`STREAM_READ_FAILURE = 4`
Description: Error while reading the stream
Action: Try again, the server may be overloaded

`VEHICLE_TIMED_OUT = 5`
Description: The vehicle timed out
Action: Try again, the server may be overloaded

`PREMATURE_LANDING = 6`
Description: The vehicle landed prematurely
Action: Wait or check the vehicle's config / payload. There may be too much wind or the vehicle can't control properly.

`UNKNOWN_VEHICLE = 7`
Description: The vehicle config is unknown
Action: Check the vehicle's name in the mission file.

`PX4_SIM_DESYNC = 8`
Description: The PX4 simulator is desynced
Action: Try again, the server may be overloaded

`TOO_MUCH_WIND = 9`
Description: There is too much wind for the vehicle to control properly
Action: Wait for better wind conditions
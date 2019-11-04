# SongFlong

## Setup
*SongFlong is built to run inside a Docker swarm and routing issues can occur if ran locally.*

To run it locally, you need to manually replace the hostname of the Redis connection. This has to be done for the main Flask app and for the Worker. Changing it to `localhost` should suffice.

To run it using Docker, all you need to do is install Docker and Docker-Compose.
```
docker-compose up --build --scale worker=3
```

The `--build` flag is not necessary; it does stuff that I don't feel like explaining to David (just look it up).
The `--scale` can be modified to replicate as many workers as you want. Removing it completely will default to just 1.
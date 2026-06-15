# Docker Commands Reference

| Command                                      | What it does                                                        |
|----------------------------------------------|---------------------------------------------------------------------|
| `docker run -it <image>`                     | Download (if needed) and start a container, attach terminal to it   |
| `docker run -it --entrypoint=bash <image>`   | Same but open a bash shell instead of the image's default program   |
| `docker ps -a`                               | Show all containers — running and stopped                           |
| `docker ps -aq`                              | List IDs of all containers (quiet mode, no extra info)              |
| `docker rm $(docker ps -aq)`                 | Delete all containers ⚠️ [use with caution — irreversible]          |
| `docker run -it --entrypoint=bash -v "$(pwd):/app" <image>` | Start a container with your current directory mounted at `/app` inside it |

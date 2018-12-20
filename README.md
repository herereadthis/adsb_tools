# Higgle

This will be a very basic primer into getting a (Python) Flask app running in a Docker Container

```bash
# Which version of Docker?
docker -v
# Which containers are running?
docker ps
# I want to kill a container
docker kill <CONTAINER_ID>
# which containers do I have?
docker images
# list containers
docker container ls -a
# stop a container
docker stop <CONTAINER_ID>
# remove a container
docker container rm <CONTAINER_ID>
# remove all stopped containers, all dangling images and all unused networks:
docker system prune
```

```
# build
docker build -t higgle:latest .
# run
# -d detaches from the run: you won't see output
# -p specifies which port it's running on
docker run -d -p 5000:5000 higgle:latest
```



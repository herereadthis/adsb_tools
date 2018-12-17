# Higgle

This will be a very basic primer into getting a (Python) Flask app running in a Docker Container

```bash
# Which version of Docker?
docker -v
# Which containers are running?
docker ps
# I want to kill a container
docker kill <CONTAINER ID>
# which containers do I have?
docker images
```

```
# build
docker build -t higgle:latest .
# run
docker run -d -p 5000:5000 higgle:latest
```

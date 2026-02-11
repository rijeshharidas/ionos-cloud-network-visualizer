FROM python:3.12-slim

LABEL maintainer="rijesh.haridas@ionos.com"
LABEL description="IONOS Cloud Network Visualizer - Interactive topology visualizer"
LABEL org.opencontainers.image.source="https://github.com/rijeshharidas/ionos-cloud-network-visualizer"
LABEL org.opencontainers.image.license="Apache-2.0"

WORKDIR /app

COPY serve.py ionos-cloud-network-visualizer.html ./

EXPOSE 8080

# --no-browser: container has no GUI
# --host 0.0.0.0: allow connections from outside the container (Docker port mapping)
CMD ["python3", "serve.py", "--no-browser", "--host", "0.0.0.0"]

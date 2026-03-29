docker build -t geoharvester .
docker run -v $(pwd)/output:/app/output geoharvester natgeo

SHORT_SHA=$(git rev-parse --short HEAD)
docker build ../.. -f Dockerfile -t zhtangsh/paimon:dev.$SHORT_SHA

SHORT_SHA=$(git rev-parse --short HEAD)
docker build ../.. -f Dockerfile -t zhtangsh/paimon:dev.$SHORT_SHA
docker tag zhtangsh/paimon:dev.$SHORT_SHA 192.168.1.50:29006/zhtangsh/paimon:dev.$SHORT_SHA
docker push 192.168.1.50:29006/zhtangsh/paimon:dev.$SHORT_SHA
all: docker-build docker-push

docker-build:
	docker build . -t wylswz/xmbsmdsj --network host

docker-push:
	docker push wylswz/xmbsmdsj
docker-release:
	docker build . -t --no-cache devopshq/artifactory-du:latest
	docker push devopshq/artifactory-du:latest

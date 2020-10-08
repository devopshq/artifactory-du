docker-release:
	docker build . --no-cache -t devopshq/artifactory-du:latest
	docker push devopshq/artifactory-du:latest

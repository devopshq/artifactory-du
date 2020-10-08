docker-release:
	docker build . -t devopshq/artifactory-du:latest
	docker push

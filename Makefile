include .env
export

export IMAGE := $(shell echo "asia-east1-docker.pkg.dev/apv-helper/cloud-run/api")

.PHONY: preview dev test format build deploy lint load

.ONESHELL:
dev:
	@trap 'npx pm2 delete real-estate-develop-assistant-api' SIGINT; npx pm2 start --no-daemon
test:
	@pytest
format:
	@autopep8 --in-place --aggressive --aggressive --recursive .
build:
	@docker buildx build --progress=plain --platform linux/amd64 . -t $${IMAGE}
push:
	@docker push $${IMAGE}
lint:
	@flake8 src/
load:
	@python main.py load --type=assessedCurrentValues --city=新北市 --year=2024
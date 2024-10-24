include .env
export

export IMAGE := $(shell echo "asia-east1-docker.pkg.dev/apv-helper/cloud-run/api")

.PHONY: preview test format build deploy lint load

.ONESHELL:
preview:
	@ENV=development python main.py serve
test:
	@pytest
format:
	@autopep8 --in-place --aggressive --aggressive --recursive .
build:
	@docker buildx build --progress=plain --platform linux/amd64 . -t $${IMAGE}
deploy:
	@docker push $${IMAGE}
lint:
	@flake8 src/
load:
	@ENV=development python main.py load --type=assessedCurrentValues --city=新北市 --year=2024
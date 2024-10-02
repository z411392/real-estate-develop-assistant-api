include .env
export

export IMAGE := $(shell echo "asia-east1-docker.pkg.dev/apv-helper/cloud-run/api")

.PHONY: preview test format build deploy lint run

.ONESHELL:
preview:
	@ENV=development python main.py -s --disable-pytest-warnings
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
run:
	@docker run --env-file=.env -it $${IMAGE} python3 main.py
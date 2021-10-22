REGISTRY := mrtaalebi
IMAGE := youtube-spam-detection
TAG ?= latest


deps:
	pip install -U poetry
	poetry install


prod-deps:
	pip install -U poetry
	poetry config virtualenvs.create false
	poetry install --no-dev --no-interaction --no-ansi


run:
	python -m youtube_spam_detection ${filter-out $@,${MAKECMDGOALS}}


%:
	@:


build:
	docker build \
		--file Dockerfile \
		--tag ${REGISTRY}/${IMAGE}:${TAG} \
		.


push:
	docker push ${REGISTRY}/${IMAGE}:${TAG}


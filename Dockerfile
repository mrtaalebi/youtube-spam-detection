
FROM python:3.9-slim

MAINTAINER mrtaalebi the.doors.are.locked@gmail.com

ENV PYTHONFAULTHANDLER=1 \
		PYTHONUNBUFFERED=1 \
		PIP_NO_CACHE_DIR=off \
		PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt update \
		&& apt install -y make

WORKDIR /youtube_spam_detection

COPY Makefile poetry.lock pyproject.toml ./

RUN make prod-deps

COPY . .

ENTRYPOINT [ "make", "run" ]
CMD [""]

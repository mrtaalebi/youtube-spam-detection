# YouTube Spam Detection

This code deletes spam comment on youtube videos based on two characteristics (currently)
- If the author of the comment has a sexually explicit profile picture
- If the comment is a duplicate of someone else's comment who has commented it earlier

## API Key
- Follow the instructions to create a google app in google developer console and get an API_KEY for that app. The google account you use for this process must be the same as the owner of the youtube channel in order to have to permissions to delete a comment.

## Arguments
- `video_id`: Part of the youtube video url between "v=" and "&" (if present)
- `dry_run`: Either `true` or `false`. If true it won't delete comments and just prints their ids
- `api_key`: You can either put the key in command line or use the instruction in following sections to keep it safer.

## Usage

### Hard Way
- You can either create a file in inner "youtube_spam_detection" folder named ".env" and put that API_KEY in it like `api_key=blablabla` or just put it in make run.
- Create a python virtual environment with `virtualenv venv --python=python3`
- Activate the venv `source venv/bin/activate`
- Install dependencies `make deps`
- Run the spam detection `make run video_id dry_run api_key`.

### Docker (Easy Way)
- Make sure you have docker installed and running.
- You can either create a docker secret and put the api_key in it or pass it in the command below.
- Run the code with `docker run -it mrtaalebi/youtube-spam-detection:latest video_id dry_run api_key`.

[Docker Image](https://hub.docker.com/repository/docker/mrtaalebi/youtube-spam-detection)

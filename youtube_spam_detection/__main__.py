import sys
import os
import json
from pathlib import Path
import hashlib
from datetime import datetime
import argparse

import requests
from googleapiclient.discovery import build
from nudenet import NudeClassifier

from youtube_spam_detection import config


def video_comments(video_id):
    video_response = youtube.commentThreads().list(
        part='snippet,replies,id',
        videoId=video_id,
    ).execute()

    comments_and_replies = []
    while video_response:
        for item in video_response['items']:
            replies = item['replies']['comments'] if 'replies' in item else []
            comments_and_replies.append(
                {
                    'comment': item_to_dict(item),
                    'replies': [
                        item_to_dict(reply, is_reply=True) for reply in replies
                    ],
                }
            )

        print('.', end='', flush=True)

        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=video_response['nextPageToken'],
            ).execute()
        else:
            break
    print()

    return comments_and_replies


def item_to_dict(item, is_reply=False):
    if is_reply:
        comment = item['snippet']
    else:
        comment = item['snippet']['topLevelComment']['snippet']
    comment['id'] = item['id']
    return comment


def delete_spam_comments(comments_and_replies, video_id):
    comments_hashed = {}
    for comment in comments_and_replies:
        for reply in [comment['comment']] + comment['replies']:
            sexaullity = get_sexually_explicit_profile_image_probability(reply)
            if sexaullity > config.sexaullity_treshold:
                delete_comment(reply['id'])

            # detect duplicates of other comments in next for
            comment_hash = hashlib.sha256(reply['textDisplay'].encode('utf-8')).hexdigest()
            if comment_hash in comments_hashed:
                comments_hashed[comment_hash].append(reply)
            else:
                comments_hashed[comment_hash] = [reply]

            print('.', end='', flush=True)
    print()

    for comments_with_same_hash in comments_hashed.values():
        str_to_time = lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')

        comments_with_same_hash.sort(
            key=lambda c: str_to_time(c['updatedAt'])
        )
        original_comment = comments_with_same_hash[0]
        for comment in comments_with_same_hash[1:]:
            if comment['authorDisplayName'] != original_comment['authorDisplayName']:
                delete_comment(comment_id)


def delete_comment(comment_id):
    if dry_run:
        print(f'spam comment detected with id: {comment_id}')
        return

    youtube.comments().delete(
        id=comment_id,
    ).execute()


def get_sexually_explicit_profile_image_probability(comment):
    save_path = save_comment_profile_image(comment)
    nudity = nude_classifier.classify(save_path)[save_path]
    os.remove(save_path)
    return nudity['unsafe']


def save_comment_profile_image(comment):
    Path(config.temp_dir).mkdir(parents=True, exist_ok=True)
    image_response = requests.get(comment['authorProfileImageUrl'])
    save_path = os.path.join(
        config.temp_dir,
        f'comment_profile_image{comment["id"]}.jpg',
    )
    with open(save_path, 'wb+') as f:
        f.write(image_response.content)
    return save_path


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('video_id', type=str)
    parser.add_argument('dry_run', type=bool, default=True)
    parser.add_argument('api_key', type=str, nargs='?', default="")
    args = parser.parse_args()

    video_id = args.video_id
    dry_run = args.dry_run
    api_key = args.api_key if args.api_key != "" else config.api_key
    if api_key is None:
        print('API_KEY is not specified. exiting.')
        exit(1)

    return api_key, video_id, dry_run


api_key, video_id, dry_run = get_args()
youtube = build('youtube', 'v3', developerKey=api_key)
comments_and_replies = video_comments(video_id)
nude_classifier = NudeClassifier()
delete_spam_comments(comments_and_replies, video_id)


import os

from dotenv import load_dotenv


load_dotenv()

api_key = os.environ.get('api_key')

comments_dir = os.environ.get('comments_dir', './comments/')
temp_dir = os.environ.get('temp_dir', './temp/')

sexaullity_treshold = float(os.environ.get('sexaullity_treshold', '0.9'))


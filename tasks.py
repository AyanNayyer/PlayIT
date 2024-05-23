from celery import shared_task
from celery import current_task
from models import Album, User, Role, Song, Album
import flask_excel as excel
from send_mail import send_email
from jinja2 import Template
from datetime import datetime, timedelta



## CSV FILE GENERATING TASK

@shared_task(ignore_result=False)
def create_resource_csv():
    album_data = Album.query.with_entities(Album.creator_name, Album.name).all()
    csv_output = excel.make_response_from_query_sets(album_data, ['creator_name', 'name'], "csv")
    filename = 'albums.csv'

    with open(filename, 'wb') as f:
        f.write(csv_output.data)

    return filename

##Mail Task

@shared_task(ignore_result=True)
def monthly_reminder():
    artists = User.query.filter(User.roles.any(Role.name == 'artist')).all()

    with open('report.html', 'r') as f:
        template = Template(f.read())
        for artist in artists:
            songs = Song.query.filter_by(creator_name = artist.username).all()
            albums = Album.query.filter_by(creator_name = artist.username).all()
            total_songs = len(songs)
            total_albums = len(albums)
            total_likes = sum(song.likes for song in songs)
            total_views = sum(song.play_count for song in songs)

            send_email(artist.email, 'Monthly Report', template.render(email= artist.email, songs= songs, total_songs= total_songs, total_albums= total_albums, total_likes= total_likes, total_views= total_views))
    
    return "Monthly Report Sent"



## WEBHOOK TASK ##

from json import dumps
from httplib2 import Http

@shared_task(ignore_result=False)
def daily_reminder():
    try:
        # datetime 24 hours ago
        timestamp = datetime.utcnow() - timedelta(hours=24)
        # not_visited_users = User.query.filter(User.last_activity < timestamp).all()

        # FOR Testing
        not_visited_users = User.query.filter(User.last_activity < datetime.utcnow()).all()
        if not not_visited_users:
            return "no inactive users today"

        for user in not_visited_users:
            username = user.username
            if username != 'admin':
                send_notification(username)

        return "Notifications sent to google chat space"
    except Exception as e:
        print(f"Error in daily_reminder task: {e}")
        return f"Error in daily_reminder task: {e}"

def send_notification(username):
    try:
        url = "https://chat.googleapis.com/v1/spaces/AAAALiWcL7A/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=VooNMr_AA3WX7_6Svxsb10rxyBAH_pUNYizsJxk61Kk"
        app_message = {"text": f"Hello {username}! You haven't visited PlayIT today. Please visit the app and enjoy the music."}
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method="POST",
            headers=message_headers,
            body=dumps(app_message),
        )
        return f"Notification sent to {username}"
    except Exception as e:
        print(f"Error in send_notification task: {e}")
        return f"Error in send_notification task: {e}"
    
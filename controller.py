from flask import current_app as app, jsonify, render_template, request, send_file
from flask_security import auth_required, roles_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Song, Album, Playlist
from databasefile import datastore
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from datetime import datetime
from celery.result import AsyncResult
from tasks import create_resource_csv
from cache import cache

## INDEX PAGE ##
@app.get('/')
def home():
    return render_template('index.html')

## ADMIN FUNCTIONS ##

@app.post('/admin_login')
def admin_login():
    input_data= request.get_json()
    input_email = input_data.get('email')
    input_password = input_data.get('password')

    if not input_email or not input_password:
        return jsonify({'message': 'Email and Password are required.'}), 400
    
    if input_email != 'admin@email.com':
        return jsonify({'message': 'Not an ADMIN!!'}), 400
    
    user = datastore.find_user(email=input_email)

    if not user:
        return jsonify({'message': 'User not found.'}), 404
    if not check_password_hash(user.password, input_password):
        return jsonify({'message': 'Incorrect Password'}), 401
    
    user.last_activity = datetime.utcnow()
    db.session.commit()
    songs = Song.query.all()
    like_graph(songs)
    genre_graph(songs)
    play_count_graph(songs)
    return jsonify({'auth_token': user.get_auth_token(), 'role': [role.name for role in user.roles]}), 200


@app.get('/app_data')
@auth_required('token')
@roles_required('admin')
@cache.cached(timeout=300)  ##start redis server first to implement caching
def app_data():
    users = User.query.all()
    all_users = [{'id': user.id, 'email': user.email, 'username': user.username, 'active': user.active, 'roles': [role.name for role in user.roles]} for user in users]
    songs = Song.query.all()
    all_songs = [{'id': song.id, 'name': song.name, 'creator_name': song.creator_name, 'album_id': song.album_id, 'album_name': Album.query.get(song.album_id).name , 'year': Album.query.get(song.album_id).year, 'lyrics': song.lyrics, 'genre': song.genre, 'duration': song.duration, 'likes': song.likes, 'play_count': song.play_count, 'flag_count': song.flag_count} for song in songs]
    albums = Album.query.all()
    all_albums = [{'id': album.id, 'name': album.name, 'creator_name': album.creator_name, 'year': album.year} for album in albums]

    return jsonify({'users': all_users, 'songs': all_songs, 'albums': all_albums}), 200


@app.post('/delete_song/<int:song_id>')
@auth_required('token')
@roles_required('admin')
def delete_song(song_id):
    song = Song.query.get(song_id)
    audio_file = 'static/audio/' + song.name + '.mp3'
    if not song:
        return jsonify({'message': 'Song not found.'}), 404
    db.session.delete(song)
    db.session.commit()
    os.remove(audio_file) 
    return jsonify({'message': 'Song deleted successfully.'}), 200


@app.post('/delete_artist/<int:artist_id>')
@auth_required('token')
@roles_required('admin')
def delete_artist(artist_id):
    artist = User.query.get(artist_id)
    if not artist:
        return jsonify({'message': 'Artist not found.'}), 404
    # delete artist from roles
    datastore.remove_role_from_user(artist, 'artist')
    db.session.commit()
    return jsonify({'message': 'Artist deleted successfully.'}), 200


@app.post('/blacklist/<int:artist_id>')
@auth_required('token')
@roles_required('admin')
def blacklist(artist_id):
    artist = User.query.get(artist_id)
    if not artist:
        return jsonify({'message': 'Artist not found.'}), 404
    # make active to be false for artist
    artist.active = False
    db.session.commit()
    return jsonify({'message': 'Artist blacklisted successfully.'}), 200


@app.post('/whitelist/<int:artist_id>')
@auth_required('token')
@roles_required('admin')
def whitelist(artist_id):
    artist = User.query.get(artist_id)
    if not artist:
        return jsonify({'message': 'Artist not found.'}), 404
    #make active to be true again 
    artist.active = True
    db.session.commit()
    return jsonify({'message': 'Artist whitelisted successfully.'}), 200



@app.post('/unflag_song/<int:song_id>')
@auth_required('token')
@roles_required('admin')
def unflag_song(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({'message': 'Song not found.'}), 404
    if song.flag_count == 0:
        return jsonify({'message': 'Song not flagged.'}), 404
    song.flag_count -= 1
    db.session.commit()
    return jsonify({'message': 'Song unflagged successfully.'}), 200



## FUNCTIONS TO GENERATE GRAPHS ##

def like_graph(songs):
    likes = [song.likes for song in songs if song.likes > 4]
    song_names = [song.name for song in songs if song.likes > 4]
    
    plt.figure(figsize=(6,3))
    plt.barh(song_names, likes , color='green')
    plt.xlabel('No. of likes', fontweight='bold')
    plt.tight_layout()
    # Save the graph as an image file in static folder
    plt.savefig('static/graphs/like_graph.png')


def genre_graph(songs):
    genre_set = set([song.genre for song in songs])
    genre = list(genre_set)
    genre_count = [len(Song.query.filter_by(genre= g).all()) for g in genre]

    plt.figure(figsize=(6,3))
    plt.barh(genre, genre_count , color='blue')
    plt.xlabel('No. of songs', fontweight='bold')
    plt.tight_layout()
    plt.savefig('static/graphs/genre_graph.png')


def play_count_graph(songs):
    play_count = [song.play_count for song in songs]
    song_names = [song.name for song in songs]

    plt.figure(figsize=(10,8))
    plt.bar(song_names, play_count , color='aqua')
    plt.ylabel('No. of times played', fontweight='bold')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('static/graphs/play_count_graph.png') 




## USER FUNCTIONS ##

@app.post('/user_register')
def user_register():
    input_data= request.get_json()
    input_email= input_data.get('email')
    input_username= input_data.get('username')
    input_password= input_data.get('password')

    if not input_email or not input_username or not input_password:
        return jsonify({'message': 'Email, Username and Password are required.'}), 400
    
    if not datastore.find_user(email=input_email):
        datastore.create_user(email=input_email, username= input_username, password= generate_password_hash(input_password), roles=['user'])
        db.session.commit()
        return jsonify({'message': 'User registered successfully. You can login now.'}), 200
    else:
        return jsonify({'message': 'Email already registered.'}), 409


@app.post('/user_login')
def user_login():
    input_data= request.get_json()
    input_email = input_data.get('email')
    input_password = input_data.get('password')

    if not input_email or not input_password:
        return jsonify({'message': 'Email and Password are required.'}), 400
    
    if input_email == 'admin@email.com':
        return jsonify({'message': 'Please Use Admin Login'}), 400
    
    user = datastore.find_user(email=input_email)

    if not user:
        return jsonify({'message': 'User not found. Register first.'}), 404
    if not check_password_hash(user.password, input_password):
        return jsonify({'message': 'Incorrect Password'}), 401
    
    if not user.active:
        return jsonify({'message': 'Your account has been blacklisted.'}), 401
    
    user.last_activity = datetime.utcnow()
    db.session.commit()
    return jsonify({'auth_token': user.get_auth_token(), 'role': [role.name for role in user.roles]}), 200


@app.get('/get_all_songs')
@auth_required('token')
@roles_required('user')
def get_all_songs():
    songs = Song.query.all()
    all_songs = [{'id': song.id, 'name': song.name, 'creator_name': song.creator_name, 'album_id': song.album_id, 'album_name': Album.query.get(song.album_id).name , 'year': Album.query.get(song.album_id).year, 'lyrics': song.lyrics, 'genre': song.genre, 'duration': song.duration, 'likes': song.likes, 'play_count': song.play_count, 'flag_count': song.flag_count} for song in songs]
    return jsonify({'songs': all_songs}), 200


@app.post('/play/<int:song_id>')
@auth_required('token')
def play(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({'message': 'Song not found.'}), 404
    song.play_count += 1
    db.session.commit()
    playing_song = [{'id': song.id, 'name': song.name, 'creator_name': song.creator_name, 'album_id': song.album_id, 'lyrics': song.lyrics, 'genre': song.genre, 'duration': song.duration, 'likes': song.likes, 'play_count': song.play_count}]
    return jsonify({'message': 'Song played successfully.', 'song': playing_song }), 200


@app.post('/like_song/<int:song_id>')
@auth_required('token')
@roles_required('user')
def like(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({'message': 'Song not found.'}), 404
    song.likes += 1
    db.session.commit()
    return jsonify({'message': 'Song liked successfully.'}), 200

@app.post('/dislike_song/<int:song_id>')
@auth_required('token')
@roles_required('user')
def dislike(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({'message': 'Song not found.'}), 404
    song.likes -= 1
    db.session.commit()
    return jsonify({'message': 'Song disliked successfully.'}), 200


@app.post('/flag_song/<int:song_id>')
@auth_required('token')
@roles_required('user')
def flag_song(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({'message': 'Song not found.'}), 404
    song.flag_count += 1
    db.session.commit()
    return jsonify({'message': 'Song flagged successfully.'}), 200


## PLAYLIST FUNCTIONS ##

@app.post('/create_playlist')
@auth_required('token')
@roles_required('user')
def create_playlist():
    user = current_user
    input_data= request.get_json()
    input_playlist_name= input_data.get('name')
    input_song_ids= input_data.get('songs')
    if not input_playlist_name or not input_song_ids:
        return jsonify({'message': 'Playlist name and songs are required.'}), 400
    if not datastore.find_user(email=user.email):
        return jsonify({'message': 'User not found.'}), 404
    
    new_playlist = Playlist(name=input_playlist_name, user_id=user.id)
    for song_id in input_song_ids:
        song = Song.query.get(song_id)
        db.session.add(new_playlist)    
        new_playlist.songs.append(song)

    db.session.commit()
    return jsonify({'message': 'Playlist created successfully.'}), 200


@app.get('/show_playlists')
@auth_required('token')
@roles_required('user')
@cache.cached(timeout=100)
def show_playlists():
    user = current_user
    playlists = Playlist.query.filter_by(user_id=user.id).all()
    return jsonify({'playlists': [{'id': playlist.id, 'name': playlist.name, 'songs': [{'id': song.id, 'name': song.name, 'creator_name': song.creator_name, 'album_id': song.album_id, 'lyrics': song.lyrics, 'genre': song.genre, 'duration': song.duration, 'likes': song.likes, 'play_count': song.play_count} for song in playlist.songs]} for playlist in playlists]}), 200


@app.post('/delete_playlist/<int:playlist_id>')
@auth_required('token')
@roles_required('user')
def delete_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({'message': 'Playlist not found.'}), 404
    db.session.delete(playlist)
    db.session.commit()
    return jsonify({'message': 'Playlist deleted successfully.'}), 200


@app.get('/open_playlist/<int:playlist_id>')
@auth_required('token')
@roles_required('user')
@cache.cached(timeout=50)
def open_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({'message': 'Playlist not found.'}), 404
    
    return jsonify({'playlist': [{'id': playlist.id, 'name': playlist.name, 'songs': [{'id': song.id, 'name': song.name, 'creator_name': song.creator_name, 'album_id': song.album_id, 'lyrics': song.lyrics, 'genre': song.genre, 'duration': song.duration, 'likes': song.likes, 'play_count': song.play_count} for song in playlist.songs]}]}), 200




## ARTIST FUNCTIONS ##

@app.post('/artist_register')
@auth_required('token')
@roles_required('user')
def artist_register():
    user = current_user
    datastore.add_role_to_user(user, 'artist')
    db.session.commit()
    return jsonify({'message': 'Artist registered successfully.', 'role': [role.name for role in user.roles] }), 200


@app.post('/upload_song')
@auth_required('token')
@roles_required('artist')
def upload_song():
    audio_file = request.files['song_file']
    file_name = request.form['file_name']
    if not audio_file:
        return jsonify({'message': 'All fields are required.'}), 400
    save_audio_file(audio_file, file_name)
    return jsonify({'message': 'Song uploaded successfully.'}), 200

def save_audio_file(file, name):
    file.save('static/audio/' + name + '.mp3')


@app.get('/your_albums')
@auth_required('token')
def your_albums():
    user = current_user

    # Fetch albums that belong to the current user
    albums = Album.query.filter_by(creator_name=user.username).all()

    #Albums as a list of dictionaries
    your_albums = [{'id': album.id, 'name': album.name, 'year': album.year} for album in albums]

    return jsonify({'albums': your_albums}), 200

@app.get('/your_uploads')
@auth_required('token')
@roles_required('artist')
def your_uploads():
    user = current_user
    songs = Song.query.filter_by(creator_name= user.username).all()
    your_songs = [{'id': song.id, 'name': song.name, 'creator_name': song.creator_name, 'album_id': song.album_id, 'album_name': Album.query.get(song.album_id).name , 'year': Album.query.get(song.album_id).year, 'lyrics': song.lyrics, 'genre': song.genre, 'duration': song.duration, 'likes': song.likes, 'play_count': song.play_count} for song in songs]
    return jsonify({'songs': your_songs}), 200
    

@app.post('/delete_upload/<int:song_id>')
@auth_required('token')
@roles_required('artist')
def delete_upload(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({'message': 'Song not found.'}), 404
    
    audio_file = 'static/audio/' + song.name + '.mp3'
    if os.path.exists(audio_file):
        os.remove(audio_file)

    db.session.delete(song)
    db.session.commit()
    
    return jsonify({'message': 'Song deleted successfully.'}), 200


@app.post('/save_changes/<int:song_id>')
@auth_required('token')
@roles_required('artist')
def save_changes(song_id):
    song = Song.query.get(song_id)
    audio_file = 'static/audio/' + song.name + '.mp3'

    new_name = request.form['song_name']
    new_album_name = request.form['album_name']
    new_genre = request.form['genre']
    new_year = request.form['year']
    new_duration = request.form['duration']
    new_lyrics = request.form['lyrics']

    if not new_name or not new_album_name or not new_genre or not new_year or not new_duration or not new_lyrics:
        return jsonify({'message': 'All fields are required.'}), 400
    
    if song.name != new_name:
        song.name = new_name
        if os.path.exists(audio_file):
            os.rename(audio_file, 'static/audio/' + new_name + '.mp3')
    if song.album.name != new_album_name:
        check_album = Album.query.filter_by(name= new_album_name).first()
        if check_album:
            return jsonify({'message': 'Album already exists.'}), 409
        else:
            song.album.name = new_album_name
    
    song.album.year = new_year
    song.genre = new_genre
    song.duration = new_duration
    song.lyrics = new_lyrics

    db.session.commit()

    return jsonify({'message': 'Changes saved successfully.'}), 200





## EXPORT CSV JOB (For Admin)

@app.get('/download')
def downloadcsv():
    task = create_resource_csv.delay()
    return jsonify({"taskid": task.id})

@app.get('/getcsv/<task_id>')
def getcsv(task_id):
    res = AsyncResult(task_id)
    if res.ready():
        filename = res.result
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({'message': 'Task pending'}), 404


##Caching Implementation    

import time
@app.route('/example_route')
@cache.cached(timeout=300)  # 300 seconds (5 minutes) cache timeout
def example_route():
    print("Executing example_route without cache")

    # Simulate a time-consuming task
    result = perform_time_consuming_task()

    return jsonify({'message': 'Route response', 'result': result})

def perform_time_consuming_task():
    result = 0
    for _ in range(1000000): 
        result += 2
        
    time.sleep(5)

    return result






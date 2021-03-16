import os
import json
from flask import Flask, session, render_template, request, jsonify
from sqlalchemy import create_engine, exc
import json

from models import *



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///audio.sqlite3'
db.init_app(app)


@app.route("/create", methods=["POST"])
def createMedia():
	resource_type = request.args.get('type')
	resource_type=resource_type.lower()
	title = request.args.get('title')
	print(title)
	duration= request.args.get('duration')
	host = request.args.get('host')
	participants = request.args.get('participants')
	narrator= request.args.get('narrator')
	author = request.args.get('author')

	if resource_type == "song":
		title = title
		duration= int(duration)
		if title is not None and duration is not None:
			try:
				song = Song(song_duration=duration, song_title=title)
			except SQLAlchemyError as e:
				print (e)
				return jsonify({
					"error": e
					}), 404
			db.session.add(song)
			db.session.commit()
			return jsonify({
				"message":" song created successfully"
				}), 201
			
		else:
			return jsonify({
				"message": "failed to create song"
				})
	elif resource_type == "podcast":
		title = title
		duration= int(duration)
		if title is not None and duration is not None and host is not None:
			try:
				podcast = Podcast(podcast_duration=duration, podcast_title=title, podcast_host=host, podcast_participants=participants)
			except SQLAlchemyError as e:
				print (e)
				return jsonify({
					"error": e
					}), 404
			db.session.add(podcast)
			db.session.commit()
			return jsonify({
				"message":"podcast created successfully"
				}), 201
			
		else:
			return jsonify({
				"message": "failed to create podcast. Did you include all params?"
				}), 422
	elif resource_type == "audiobook":
		title = title
		duration= int(duration)
		if title is not None and duration is not None and narrator is not None and author is not None:
			try:
				audiobook = AudioBook(audiobook_duration=duration, audiobook_title=title, narrator=narrator, book_author=author)
			except SQLAlchemyError as e:
				print (e)
				return jsonify({
					"error": e
					}), 422
			db.session.add(audiobook)
			db.session.commit()
			return jsonify({
				"message":"audiobook created successfully"
				}), 201
			
		else:
			return jsonify({
				"message": "failed to create audiobook. Did you include all params?"
				}), 422

@app.route("/<audio_type>")
@app.route("/<audio_type>/<int:resource_id>", methods=['GET','DELETE'])
def get_audio(audio_type, resource_id=None):
	audio_type=audio_type.lower()
	if request.method == 'DELETE':
		if audio_type=="song" and resource_id is not None:
			try:
				resource = Song.query.get(resource_id)
				if resource is None:
					return jsonify({
						"error":"sorry I couldn't find the resource"
						}), 404
				db.session.delete(resource)
				db.session.commit()
				return jsonify({
					"message":"resource deleted successfully"
					}), 204
			except SQLAlchemyError as e:
				print(e)
		elif audio_type=="podcast" and resource_id is not None:
			try:
				resource = Podcast.query.get(resource_id)
				if resource is None:
					return jsonify({
						"error":"sorry I couldn't find the resource"
						}), 404
				db.session.delete(resource)
				db.session.commit()
				return jsonify({
					"message":"resource deleted successfully"
					}), 204
			except SQLAlchemyError as e:
				print(e)
		elif audio_type=="audiobook" and resource_id is not None:
			try:
				resource = AudioBook.query.get(resource_id)
				if resource is None:
					return jsonify({
						"error":"sorry I couldn't find the resource"
						}), 404
				db.session.delete(resource)
				db.session.commit()
				return jsonify({
					"message":"resource deleted successfully"
					}), 204
			except SQLAlchemyError as e:
				print(e)


	if audio_type=="song" and resource_id is not None:
		resource_id =int(resource_id)
		try:
			song = Song.query.get(resource_id)
			if song is None:
				return jsonify({
					"error": "resource not found"
					}), 404
			return jsonify({
				"id":song.id,
				"title": song.song_title,
				"duration": song.song_duration,
				"date": song.song_upload_date
				})
		except SQLAlchemyError as e:
			print (e)
	elif audio_type == "song" and resource_id is None:	
		try:
			resource = Song.query.all()
			if resource is None:
				return jsonify({
					"error": "No resource of type song found"
					}), 404
			result=[]
			for song in resource:
				title = song.song_title
				duration= song.song_duration
				date = song.song_upload_date
				result.append(title)
				result.append(duration)
				result.append(date)
			data = {}
			for x in result:
				data["song"]=result
			return data
		except exc.SQLAlchemyError as error:
			print(error)
	elif audio_type== "podcast" and resource_id is not None:
		try:
			podcast= Podcast.query.get(resource_id)
			if podcast is None:
				return jsonify({"error": "resource not found"}), 404
			return jsonify({
				"id": podcast.id,
				"title": podcast.podcast_title,
				"duration": podcast.podcast_duration,
				"date": podcast.podcast_upload_time,
				"host": podcast.podcast_host,
				"participants":podcast.podcast_participants
				})
		except SQLAlchemyError as e:
			print(e)
	elif audio_type=="podcast" and resource_id is None:
		try:
			podcasts = Podcast.query.all()
			if podcasts is None:
				return jsonify({"error": "Resource not found"}), 404
			result=[]
			for podcast in podcasts:
				title = podcast.podcast_title
				duration= podcast.podcast_duration
				date = podcast.podcast_upload_time
				host = podcast.podcast_host
				result.append(title)
				result.append(duration)
				result.append(date)
				result.append(host)
			data = {}
			for x in result:
				data["podcast"]=result
			return data
		except exc.SQLAlchemyError as error:
			print(error)
	elif audio_type== "audiobook" and resource_id is not None:
		try:
			audiobook= AudioBook.query.get(resource_id)
			if audiobook is None:
				return jsonify({"error": "Resource not found"}), 404
			return jsonify({
				"id": audiobook.id,
				"title": audiobook.audiobook_title,
				"duration": audiobook.audiobook_duration,
				"date": audiobook.audiobook_upload_date,
				"author": audiobook.book_author,
				"narrator": audiobook.narrator
				}), 200
		except exc.SQLAlchemyError as e:
			print(e)
	elif audio_type=="audiobook" and resource_id is None:
		try:
			audiobooks = AudioBook.query.all()
			if audiobooks is None:
				return jsonify({"error": "Resource not found"}), 404
			result=[]
			for audiobook in audiobooks:
				title = audiobook.audiobook_title
				duration= audiobook.audiobook_duration
				date = audiobook.audiobook_upload_date
				narrator = audiobook.narrator
				author = audiobook.book_author
				result.append(title)
				result.append(duration)
				result.append(date)
				result.append(narrator)
				result.append(author)
			data = {}
			for x in result:
				data["podcast"]=result
			return data
		except exc.SQLAlchemyError as error:
			print(error)
@app.route('/<audio_type>/<int:resource_id>', methods=['PUT'])
def updateResource(audio_type, resource_id):
	title = request.args.get('title')
	print(title)
	duration= request.args.get('duration')
	host = request.args.get('host')
	participants = request.args.get('participants')
	narrator= request.args.get('narrator')
	author = request.args.get('author')
	if audio_type == "song":
		try:
			song = Song.query.get(resource_id)

			if song is None:
				return jsonify({
					"error":"Resource not found"
					}), 404
			if title is not None:
				song.song_title=title
			if duration is not None:
				song.song_duration=int(duration)
			db.session.commit()
			return jsonify({
				"message":"song updated"
				}), 201
				
		except exc.SQLAlchemyError as e:
			return jsonify({
					"message":"no changes were made"
					}), 422
			print (e)
	if audio_type == "podcast":
		try:
			podcast = Podcast.query.get(resource_id)

			if podcast is None:
				return jsonify({
					"error":"Resource not found"
					}), 404
			if title is not None:
				podcast.podcast_title=title
			if duration is not None:
				podcast.podcast_duration=int(duration)
			if participants is not None:
				podcast.podcast_participants= participants
			if host is not None:
				podcast.podcast_host= host
			db.session.commit()
			return jsonify({
				"message":"podcast updated"
				}), 201
				
		except exc.SQLAlchemyError as e:
			return jsonify({
					"message":"no changes were made"
					}), 422
			print (e)
	if audio_type == "podcast":
		try:
			audiobook = AudioBooks.query.get(resource_id)

			if audiobook is None:
				return jsonify({
					"error":"Resource not found"
					}), 404
			if title is not None:
				audiobook.audiobook_title=title
			if duration is not None:
				audiobook.audiobook_duration=int(duration)
			if narrator is not None:
				audiobook.narrator= narrator
			if author is not None:
				audiobook.book_author= author
			db.session.commit()
			return jsonify({
				"message":"audiobook updated"
				}), 201
				
		except exc.SQLAlchemyError as e:
			return jsonify({
					"message":"no changes were made"
					}), 422
			print (e)
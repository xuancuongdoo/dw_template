from flask_pymongo import PyMongo
import os
import gridfs
import pika
import json
from flask import request, Flask
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host:minikube.internal:27017/videos"

mongo = PyMongo(server)
fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        "rabbitmq"
    ))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token, 200
    else:
        return err, 401


@server.route("/upload", methods="POST")
def upload():
    access, err = validate.token(request)

    access = json.loads(access)
    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "Only one file allowed", 400
        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access)

            if err:
                return err
        return "Success", 200
    else:
        return "not authorized", 401

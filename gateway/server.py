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
server.config["MONGO_URI"] = "mongodb:/host:minikube.internal:27017/videos"


mongo = PyMongo(server)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='minikube.internal'))
channel = connection.channel()


@server.route("/login",  methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token, 200
    else:
        return err, 404


@server.route("/upload", methods="POST")
def upload():
    access, err = validate.token(request)

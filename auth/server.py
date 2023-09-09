import jwt
import datetime
import os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# configuration
server.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
server.config['MYSQL_USER'] = os.environ['MYSQL_USER']
server.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
server.config['MYSQL_DB'] = os.environ['MYSQL_DB']
server.config['MYSQL_PORT'] = os.environ['MYSQL_PORT']


@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return 'Unauthorized', 401

    cur = mysql.connection.cursor()

    res = cur.execute(
        "SELECT email, password FROM users WHERE email = %s", (auth.username,)
    )

    if res > 0:
        user = cur.fetchone()
        password = user[1]
        email = user[0]

        if (auth.username, auth.password) != (email, password):
            return 'Unauthorized', 401
        else:
            token = create_jwt(auth.username, os.environ['SECRET_KEY'], True)
            return token
    else:
        return "Unauthorized", 401


@server.route('/validate', methods=['POST'])
def validate():
    encoded_jwt = request.headers.get['Authorization']

    if not encoded_jwt:
        return 'Unauthorized', 401

    encoded_jwt = encoded_jwt.split(' ')[1]
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ['SECRET_KEY'], algorithms=['HS256'])
    except:
        return 'Unauthorized', 403
    return decoded, 200


def create_jwt(usrname, secret_key, authz):
    token = jwt.encode(
        {
            'user': usrname,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'is_admin': authz
        },
        secret_key,
        algorithm='HS256'
    )
    return token


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000, debug=True)

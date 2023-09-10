import pika
import json


def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as e:
        return "Internal Server Error", 500

    message = {
        "fid": fid,
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as e:
        fs.delete(fid)
        return "Internal Server Error", 500

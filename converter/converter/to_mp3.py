import pika
import json
import tempfile
import os
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_video, fs_mp3, channels):
    message = json.loads(message)

    tf = tempfile.NamedTemporaryFile()
    tf.write(message['video'])
    out = fs_video.get(ObjectId(message['video_id']))

    tf.write(out.read())

    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    tf_path = tempfile.gettempdir() + f"/{message['video_id']}.mp3"
    audio.write_audiofile(tf_path)

    # save to mongo
    with open(tf_path, "rb") as f:
        data = f.read()
        fid = fs_mp3.put(data)
    os.remove(tf_path)

    message["mp3_fid"] = str(fid)

    try:
        channels.basic_publish(
            exchange='',
            routing_key=os.environ['MP3_QUEUE'],
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        fs_mp3.delete(fid)
        return f"got {err} failed to publish message "

import json
import logging
import os
import uuid
import boto3

from flask import Flask, request
from utils import success_json_response
from error_handler import error_handler, BadRequestException

s3 = boto3.client("s3")

def check_environment():
  if "BUCKET" not in os.environ:
    logger.error("Missing BUCKET environment variable")
    exit(-1)

check_environment()

BUCKET = os.environ.get("BUCKET")

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s')
logger = logging.getLogger(__name__)

@app.route("/")
def root():
  return success_json_response({
    "ping": "pong"
  })

@app.route("/event/<string:app>", methods=["POST"])
@error_handler
def log_event(app):
  if request.json:
    localdict = request.json
    localdict["id"] = str(uuid.uuid4())
    s3.put_object(
      Body=json.dumps(localdict),
      Bucket=BUCKET,
      Key="{app}/{id}".format(app=app, id=localdict["id"])
    )
    return(success_json_response(localdict))
  else:
    raise BadRequestException("Request should be JSON")

if __name__ == "__main__":
  app.run(debug=False, host="0.0.0.0", port=5001, threaded=True)
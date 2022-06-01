import hmac
import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask import request

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


app = Flask(__name__)
API_NAME = os.getenv('API_NAME')
API_DESCRIPTION = os.getenv('API_DESCRIPTION')
API_VERSION = os.getenv('API_VERSION')
DEPLOY_COMMAND = os.getenv('DEPLOY_COMMAND')
GITHUB_WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')


def verify_signature():
    header_signature = request.headers.get('X-Hub-Signature-256')

    if not header_signature:
        return False

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha256':
        return False

    local_signature = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=request.get_data(), digestmod='sha256')
    return hmac.compare_digest(local_signature.hexdigest(), signature)


@app.route('/')
def index():
    return {
        'name': API_NAME,
        'description': API_DESCRIPTION,
        'version': API_VERSION,
    }


@app.route('/deploy', methods=['POST'])
def deploy():
    verified = verify_signature()

    if not verified:
        return {
            'message': 'The request could not be verified. Signature missing or does not match.',
            'verified': False,
        }, 400

    subprocess.call(DEPLOY_COMMAND, shell=True)

    return {
        'message': 'Deploying...',
        'verified': True,
    }


if __name__ == '__main__':
    app.run()

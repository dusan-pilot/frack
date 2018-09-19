import ast
import os
from flask import (Flask, jsonify, render_template, request, abort)
from logger import configure_logging
import utils
from cryptography.fernet import Fernet


# CREATE FLASK APP
app = Flask(__name__)

# LOAD ENV VARS
app.config.from_pyfile('.env', silent=True)

# LOGGER
configure_logging(
    app.config['LOG_TO_FILE']
    if 'LOG_TO_FILE' in app.config.keys()
    else True
)


# ROUTES

@app.route('/')
def index():
    app.logger.info('Index page requested.')
    return render_template('index.json'), 200, {
        'Content-Type': 'application/json'}


@app.route('/slash', methods=['POST'])
def slash():
    secret = os.environ.get('SLACK_SIGNING_SECRET', None)
    if not secret:
        app.logger.error('Env var slack signing secret not found. Aborting...')
        abort(jsonify(text="Frack service: SLACK SECRET MISSING!!"))

    slack_request_verified = utils.verify_slack_request(request, secret)

    if slack_request_verified:
        app.logger.info('Slack request verified.')
        url = request.form['text']
        app_hash = utils.extract_data(url)
        if app_hash:
            url_root = request.url_root[:-1]
            query_params = dict(hash=app_hash, fileUrl=url)
            frack_secret = os.environ.get('FRACK_SECRET', "pNKgn5yGMrkdQUp_2HTAD6VKmRUv3tE7a5gXkkrCkQU=")  # noqa
            f = Fernet(frack_secret)
            cypher_query_string = f.encrypt(str(query_params))
            frame_app_url = '{}/frame?app={}'.format(
                url_root, cypher_query_string)
            payload = utils.generate_payload(frame_app_url)
            app.logger.info('URL sent to Slack. [{}]'.format(frame_app_url))
            return jsonify(payload)
        else:
            app.logger.error(
                'URL [{}] cannot be validated. Aborting...'.format(url))
            abort(400)
    else:
        app.logger.error('Slack request cannot be verified. Aborting...')
        abort(401)


@app.route('/frame', methods=['GET'])
def frame():
    token = os.environ.get('FRAME_TOKEN', None)
    if not token:
        app.logger.error('Env var frame token not found. Aborting...')
        abort(jsonify(text="Frack service: FRAME TOKEN MISSING!!"))
    frack_secret = os.environ.get('FRACK_SECRET', "pNKgn5yGMrkdQUp_2HTAD6VKmRUv3tE7a5gXkkrCkQU=")  # noqa
    f = Fernet(frack_secret)
    query_params_string = f.decrypt(str(request.args.get('app')))
    data_dict = ast.literal_eval(query_params_string)
    payload = [
        str(data_dict['hash']),
        str(data_dict['fileUrl']),
        token
    ]

    return render_template('layout.html', payload=payload)


# ERROR HANDLERS

@app.errorhandler(400)
def custom_400(error):
    return render_template('400.json'), 200, {
        'Content-Type': 'application/json'}


@app.errorhandler(401)
def custom_401(error):
    return render_template('401.json'), 200, {
        'Content-Type': 'application/json'}


# ENTRY POINT
if __name__ == '__main__':
    app.run()

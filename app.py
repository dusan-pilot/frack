from flask import Flask, jsonify, render_template
from logger import configure_logging

# create flask app
app = Flask(__name__)

# load secret env variables
app.config.from_pyfile('.env', silent=True)

# logger
configure_logging(
    app.config['LOG_TO_FILE']
    if 'LOG_TO_FILE' in app.config.keys()
    else True
)


# ROUTES


@app.route('/')
def index():
    """Display frack's index page."""
    app.logger.info('index page requested')
    return render_template('index.html')


@app.route('/frame', methods=['POST'])
def frame():
    """Return simple JSON payload to Slack"""
    payload = {'text': 'Hello Frack!'}
    return jsonify(payload)


if __name__ == '__main__':
    app.run()

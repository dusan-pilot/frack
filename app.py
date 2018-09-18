from flask import Flask, jsonify, render_template

# create flask app
app = Flask(__name__, instance_relative_config=True)
# use instance directory to store secret env variables
app.config.from_pyfile('config.py', silent=True)


# ROUTES

@app.route('/')
def index():
    """Display frack's index page."""
    return render_template('index.html')


@app.route('/frame', methods=['POST'])
def frame():
    """Return simple JSON payload to Slack"""
    payload = {'text': 'Hello Frack!'}
    return jsonify(payload)


if __name__ == '__main__':
    app.run()

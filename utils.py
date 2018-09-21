import os
import hmac
import hashlib
import logging
import urllib2


logger = logging.getLogger()


def verify_slack_request(request, secret):
    ts = request.headers['X-Slack-Request-Timestamp']
    slack_signature = request.headers['X-Slack-Signature']
    data = request.get_data()
    logger.info(
        'Verifying request from: {}: '.format(request.form['user_name']))
    sig_basestring = 'v0:{}:{}'.format(str(ts), data)
    digest = hmac.new(secret,
                      msg=sig_basestring,
                      digestmod=hashlib.sha256).hexdigest()
    signature = 'v0={}'.format(digest)
    return signature == slack_signature


def extract_data(text):
    if text and text != "":
        if file_exists(text):
            ext = os.path.splitext(text)[1]
            app_hash = os.environ.get(ext[1:].upper(), None)
            logger.info('ext: {} app_hash: {}'.format(ext, app_hash))
        else:
            logger.warning('File doesn\'t exist.')
            return None

        if app_hash:
            logger.debug('Application hash [{}] found.'.format(app_hash))
            return app_hash
        else:
            logger.warning('Extension not supported.')
            return None
    else:
        logger.warning('Empty command submitted.')
        return None


def generate_payload(frame_app_url):
    payload = {
        'text': 'Your Frame app is ready!',
        'attachments': [
            {
                'fallback': 'Frame app is ready!',
                'color': '#36a64f',
                'title': 'Open frame app.',
                'title_link': frame_app_url
            }
        ]
    }
    return payload


def file_exists(url):
    request = urllib2.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except:
        return False

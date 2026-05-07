import socket
import time

from flask import Flask, request, jsonify

from coar import validate_coar_request, handle_request
from masto import get_config
from errors import Error
app = Flask(__name__)
host = socket.gethostname()

@app.route('/')
def root():
    return f'''<!DOCTYPE HTML>    
    {dashboard()}
    '''

@app.route('/inbox', methods=['POST'])
def inbox():
    coar_request = validate_coar_request(post_request=request)
    handle_request(coar_request)

    return success(code=201, message={"status": "COAR Notify message ingested", "source": coar_request})

@app.route('/outbox')
def outbox():
    return f'''<!DOCTYPE HTML>
    {outbox_status()}
    '''

@app.route('/config')
def config():
    conf = get_config()
    content = "\n" + "\n".join([
        conf[section]["API_TOKEN"][0:5] + " @ " + conf[section]["API_URL"]
        + " | " + section
         for section in conf.sections()
    ])

    return f'''<!DOCTYPE HTML>
    <pre>
    Configured Masto Relays
    {content}
    </pre>
    '''

@app.route('/doc')
def doc():
    return f'''<!DOCTYPE HTML>
    <pre>
{open("README.md").read()}

    See <a href="https://github.com/ofa-lab/coar2masto">source code on github</a>.
    </pre>
    '''

# -------------------------

def dashboard():
    return f'''
    <pre>
    Welcome to the « COAR 2 Masto » half-bridge
    
    Available endpoints:
    
    * <a href="/inbox">/inbox</a> (POST)
    * <a href="/outbox">/outbox</a>
    * <a href="/config">/config</a>
    
    * <a href="/doc">/doc</a>
    
    status: {status()}, host: {host}
    </pre>
    '''


def outbox_status():
    return f'''
    <pre>
    <a href="https://piaille.fr/@coar2masto">@coar2masto@piaille.fr</a>
    </pre>
    '''


def status():
    return f"UP for {up_time_minutes()} minutes"


start_time = time.time()

def up_time_minutes():
    return round((time.time() - start_time)/60)


def success(code: int, message):
    return jsonify(message), code

@app.errorhandler(Error)
def error_handler(e: Error):
    return jsonify({"error": e.code, "message": e.message}), e.code


if __name__ == '__main__':
    app.run(host="0.0.0.0")

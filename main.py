import flask
import requests
#import os

app = flask.Flask(__name__)

method_requests_mapping = {
    'GET': requests.get,
    'HEAD': requests.head,
    'POST': requests.post,
    'PUT': requests.put,
    'DELETE': requests.delete,
    'PATCH': requests.patch,
    'OPTIONS': requests.options,
}

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(app.root_path+"/",
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return 'Usage: https://secure--adcharity.repl.co/https://www.google.com/<br>Use only <b>one</b> slash after protocol'

@app.route('/<path:url>', methods=method_requests_mapping.keys())
def proxy(url):
    url=url.replace("/","//",1)    
    requests_function = method_requests_mapping[flask.request.method]
    request = requests_function(url, stream=True, params=flask.request.args)
    response = flask.Response(flask.stream_with_context(request.iter_content()),
                              content_type=request.headers['content-type'],
                              status=request.status_code)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=8080)

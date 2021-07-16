from flask import Flask, jsonify, request
from flask.helpers import make_response
from functools import wraps
from datetime import datetime
import psutil, ast, sys


app = Flask(__name__)


m = {
    'Time': lambda: datetime.now().strftime('%d-%m-%y  %H:%M:%S'),
    'CPU': lambda: f'{psutil.cpu_percent()} %',
    'RAM': lambda: f'{psutil.virtual_memory().available * 100 / psutil.virtual_memory().total:.2f} %',
    'Disk': lambda: f"{psutil.disk_usage('/').percent} %",
    'Network': lambda: {
        'received': f'{float(psutil.net_io_counters().bytes_recv) * 10 ** -6:.2f} Mb',
        'sent': f'{float(psutil.net_io_counters().bytes_sent) * 10 ** -6:.2f} Mb',
    }
}


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'user' and auth.password == 'pass':
            return f(*args, **kwargs)
        return make_response('Bad credentials', 401, {'WWW-Authenticate': 'Basic realm = "Login Required"'})
    return decorated
 

@app.route('/run', methods=['GET'])
@auth_required
def get_updated_dict():
    '''Routing /run displays JSON with parameters of CPU, RAM, Disk & Network usage of current container.'''
    with open('Dictionary.txt') as f:
        indicators = ast.literal_eval(f.read())

    if not indicators:
        return -1

    info = {k: m[k]() for k in indicators.keys()}

    print(info, sys.stderr)
    return jsonify(info)
 

if __name__ == '__main__':
    app.run(debug='true')
   
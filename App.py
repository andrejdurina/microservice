from flask import Flask,jsonify,request
from flask.helpers import make_response
from functools import wraps
import psutil,ast,sys

app = Flask(__name__)

def auth_required(f):
        @wraps(f)
        def decorated(*args,**kwargs):
                auth=request.authorization
                if auth and auth.username == 'user' and auth.password == 'pass':
                        return f(*args,**kwargs)
                return make_response('Bad credentials',401,{'WWW-Authenticate' : 'Basic realm = "Login Required"'})
        return decorated

""""Creates dictionary from.txt with key values"""
file = open("Dictionary.txt","r")
contents = file.read()
indicators = ast.literal_eval(contents)

"""Basic home routing"""
@app.route("/",methods=["GET"])
def home():
  return "Welcome to testing page, to advance append /run to url!"

"""Routing /run displays JSON with parameters of CPU,RAM,Disk & Network usage of current container."""
@app.route("/run", methods=["GET","POST"])
@auth_required
def get_updated_dict():
     if not indicators:
        return -1
     else:
        for key in indicators.keys():
            if (key == "CPU"):
                    indicators[key] = str(psutil.cpu_percent())
            if (key == "RAM"):
                    indicators[key] = str(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
            if (key == "Disk"):
                    indicators[key] = str(psutil.disk_usage('/').percent)
            if (key == "Network"):
                    indicators[key]['recieved'] = str(float(psutil.net_io_counters().bytes_recv)*10 ** -6)
                    indicators[key]['sent'] = str(float(psutil.net_io_counters().bytes_sent)*10 ** -6) # In Megabytes
        print(indicators,sys.stdout)
     return jsonify(indicators)
 
if __name__ == "__main__":
  app.config['BASE_AUTH_FORCE'] = True
  app.run(debug="true")
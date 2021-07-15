from flask import Flask,jsonify
import psutil,ast,sys

app = Flask(__name__)

""""Creates dictionary from.txt with key values"""
file = open("Dictionary.txt","r")
contents = file.read()
indicators = ast.literal_eval(contents)

"""Basic home routing"""
@app.route("/",methods=["GET"])
def home():
  return "Welcome to HomePage!"

"""Routing /run displays JSON with parameters of CPU,RAM,Disk & Network usage of current container."""
@app.route("/run", methods=["GET","POST"])
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
                    indicators[key]['recieved'] = str(psutil.net_io_counters().bytes_recv)
                    indicators[key]['sent'] = str(psutil.net_io_counters().bytes_sent)
        print(indicators,sys.stdout)
     return jsonify(indicators)
 
if __name__ == "__main__":
  app.run(debug="true")

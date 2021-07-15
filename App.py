from flask import Flask,jsonify
import psutil,ast

app = Flask(__name__)

file = open("Dictionary.txt","r")
contents = file.read()
indicators = ast.literal_eval(contents)

"""Basic home routing"""
@app.route("/",methods=["GET"])
def home():
  return "Welcome to HomePage!"

"""" Observer https://www.geeksforgeeks.org/observer-method-python-design-patterns/"""
class Subject:
    def __init__(self):
        self._observers = []
 
    def notify(self, modifier = None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
 
    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
  
class Data(Subject):

    def __init__(self, name =''):
        Subject.__init__(self)
        self.name = name
        self._data = 0
 
    @property
    def data(self):
        return self._data
 
    @data.setter
    def data(self, value):
        self._data = value
        self.notify()

"""Routing /performance displays JSON with parameters of CPU,RAM,Disk & Network usage of current machine."""
@app.route("/performance", methods=["GET","POST"])
def get_updated_dict():
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
  return jsonify(indicators),201

if __name__ == "__main__":
  app.run(debug="true")
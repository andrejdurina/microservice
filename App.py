from flask import Flask
app = Flask(__name__)
app.config["DEBUG"] = true

indicators = [
  {'name': 'CPU',
   'usage' : 25,},
  { 'name' : 'RAM'
    'usage' : 50,}
  { 'name' : 'DISK'
    'usage' : 50,}
  { 'name' : 'NETWORK'
    'usage' : 50,}
    ]

@app.route("/",methods["GET"])
def home():
  return "Welcome to HomePage!"

@app.route("/performance", methods["GET"])
def sendData():
  return jsonify(indicators)


if __name__ == "__main__":
  app.run()
  
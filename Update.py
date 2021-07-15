import psutil,ast
class Update:
    def get_updated_dict():
        file = open("Dictionary.txt","r")
        contents = file.read()
        indicators = ast.literal_eval(contents)
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
        return indicators
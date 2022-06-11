# importing the requests library
import requests, json
from requests.auth import HTTPBasicAuth
import matplotlib.pyplot as plt
import numpy as np


class ReadApi:
    def __init__(self):
        self.URL = "https://analyzer-app-i524883.cfapps.sap.hana.ondemand.com/getMetrics"
        self.username = "lovish.mehta@sap.com"
        self.password = "123456"
    
    def requestData(self):
        request_object = requests.get(url = self.URL, auth = HTTPBasicAuth(self.username, self.password))
        # extracting data in json format
        if request_object.status_code == 200:
            data = request_object.json()
        else:
            raise Exception("Error code returned:{}", request_object)
        return data

class Plotter:
    def __init__(self):
        readApi = ReadApi()
        self.json_data = readApi.requestData()
        if not self.json_data:
            raise Exception("The data returned from API is empty. Cannot create plots")
        else:
            self.writeJson()

        self.time_stamps = list()
        self.cpu_time = list()
        self.memory = list()
        self.consumer_lag_p0 = list()
        self.consumer_lag_p1 = list()
        self.consumer_lag_p2 = list()
        self.processJson()

    def processTime(self, time):
        time = time.split(" ")[1]
        time = time.split(":")[2]
        return time

    def processJson(self):
        if "METRICS" not in self.json_data:
            raise Exception("Metrics data not in json object")
        
        for metric in self.json_data["METRICS"]:
            time = metric["TIMESTAMP"]
            time = self.processTime(time)
            self.time_stamps.append(float(time))
            self.cpu_time.append(metric["CPU"])
            self.memory.append(metric["MEMORY"])
            self.consumer_lag_p0.append(metric["CONSUMERLAG"]["P0"])
            self.consumer_lag_p1.append(metric["CONSUMERLAG"]["P1"])
            self.consumer_lag_p2.append(metric["CONSUMERLAG"]["P2"])

        self.cpu_time = [float(i) for i in self.cpu_time]
        self.memory = [float(i) for i in self.memory]
        self.consumer_lag_p0 = [float(i) for i in self.consumer_lag_p0]
        self.consumer_lag_p1 = [float(i) for i in self.consumer_lag_p1]
        self.consumer_lag_p2 = [float(i) for i in self.consumer_lag_p2]
        print(self.time_stamps)

    def writeJson(self):
        # Serializing json 
        json_object = json.dumps(self.json_data, indent = 4)  
        # Writing to sample.json
        with open("requestObject.json", "w") as outfile:
            outfile.write(json_object)

    def plotTimeVSCPU(self):
        time_intervals = list(range(0, len(self.time_stamps)))
        plt.xticks(np.arange(min(self.time_stamps), max(self.time_stamps), 4.0))
        plt.figure(100)
        print((min(self.time_stamps), max(self.time_stamps)))
        plt.plot(time_intervals, self.cpu_time)
        plt.xlabel("Timestamp")
        plt.ylabel("Cpu")
        plt.savefig('cpu.png')
    
    def plotTimeVSMemory(self):
        time_intervals = range(0, len(self.time_stamps))
        #plt.xticks(self.time_stamps)
        plt.xticks(np.arange(min(self.time_stamps), max(self.time_stamps), 4.0))
        plt.figure(200)
        print(self.memory)
        plt.plot(time_intervals, self.memory)
        plt.xlabel("Timestamp")
        plt.ylabel("Memory")
        plt.savefig('memory.png')

    def plotTimeVSConsumerLagP0(self):
        time_intervals = range(0, len(self.time_stamps))
        plt.xticks(np.arange(min(self.time_stamps), max(self.time_stamps), 4.0))
        #plt.xticks(self.time_stamps
        plt.figure(300)
        plt.plot(time_intervals, self.consumer_lag_p0)
        plt.xlabel("Timestamp")
        plt.ylabel("ConsumerLag(P0)")
        plt.savefig('p0.png')

    def plotTimeVSConsumerLagP1(self):
        time_intervals = range(0, len(self.time_stamps))
        plt.xticks(np.arange(min(self.time_stamps), max(self.time_stamps), 4.0))
        #plt.xticks(self.time_stamps)
        plt.figure(400)
        plt.plot(time_intervals, self.consumer_lag_p1)
        plt.xlabel("Timestamp")
        plt.ylabel("ConsumerLag(P1)")
        plt.savefig('p1.png')

    def plotTimeVSConsumerLagP2(self):
        time_intervals = range(0, len(self.time_stamps))
        plt.xticks(np.arange(min(self.time_stamps), max(self.time_stamps), 4.0))
        #plt.xticks(self.time_stamps)
        plt.figure(500)
        plt.plot(time_intervals, self.consumer_lag_p2)
        plt.xlabel("Timestamp")
        plt.ylabel("ConsumerLag(P2)")
        plt.savefig('p2.png')

plotter = Plotter()
plotter.plotTimeVSCPU()
plotter.plotTimeVSMemory()
plotter.plotTimeVSConsumerLagP0()
plotter.plotTimeVSConsumerLagP1()
plotter.plotTimeVSConsumerLagP2()



# 
# Example file for parsing and processing JSON
# LinkedIn Learning Python course by Joe Marini
#

import urllib.request
import json

def printResults(localData):
    # get local data to dictionary
    localDataJson = json.loads(localData)
    
    localUrl = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/" #1010500.json"
    
    localDic = dict()

    for tmp in localDataJson["data"]:
        # get url data
        urlPath = localUrl + str(tmp["globalIdLocal"]) + ".json"
        # print(urlPath)
        
        webUrl = urllib.request.urlopen(urlPath)
        code = webUrl.getcode()
        
        if (code == 200):
            cityInfo = json.loads(webUrl.read())
            
            for t in cityInfo["data"]:
                print("Cidade", tmp["local"], " T. Min:", t["tMin"], " T. Max:", t["tMax"], " Data:", t["forecastDate"])
                
        # localDic.append({"id": tmp["globalIdLocal"], "city": tmp["local"]})
        # localDic[tmp["globalIdLocal"]] = tmp["local"]
        # print()
    
    # print(localDic.__len__)
        
    # Use the json module to load the string data into a dictionary
    # theJSON = json.loads(data)
    
    # now we can access the contents of the JSON like any other Python object
    # if ("title" in theJSON["metadata"]):
    #     print(theJSON["metadata"]["title"])
    
    # output the number of events, plus the magnitude and each event name  
    # count = theJSON["metadata"]["count"]
    # print(count, "events recorded")
    
    # for each event, print the place where it occurred
    # for dictionary in theJSON:
    #     print(dictionary)
    #     for value in theJSON[dictionary]:
    #         print(value)
    #         if (theJSON[dictionary] != None and theJSON[dictionary][value] != None ):
    #             print("Temperatura:", theJSON[dictionary][value]["temperatura"])

    # print("-------------------------\n")
    # print the events that only have a magnitude greater than 4
    # for dictionary in theJSON:
    #     for value in theJSON[dictionary]:
    #         if (theJSON[dictionary] != None and theJSON[dictionary][value] != None ):
    #             temp = float(theJSON[dictionary][value]["temperatura"])
                
    #             if (str(value) in localDic):
    #                 city = localDic[value]
                
    #                 print("Cidade", city, " com a temperatura de :", theJSON[dictionary][value]["temperatura"])

    # print only the events where at least 1 person reported feeling something

  
def main():
    # define a variable to hold the source URL
    # In this case we'll use the free data feed from the USGS
    # This feed lists all earthquakes for the last day larger than Mag 2.5
    urlLocal = "https://api.ipma.pt/open-data/distrits-islands.json"
    # urlData = "https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json"
    # urlData = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"

    # get local json
    webLocalUrl = urllib.request.urlopen(urlLocal)
    codeLocal = webLocalUrl.getcode()
    print ("result code 1: " + str(codeLocal))
    
    # Open the URL and read the data
    # webUrl = urllib.request.urlopen(urlData)
    # code = webUrl.getcode()
    # print ("result code 2: " + str(code))
    
    # if (code == 200 and codeLocal == 200):
    if (codeLocal == 200):
        # printResults(webUrl.read(), webLocalUrl.read())
        printResults(webLocalUrl.read())
    else:
        print("Receive an error from the server:", codeLocal)
  

if __name__ == "__main__":
    main()

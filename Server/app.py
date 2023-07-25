#!flask/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
from flask import Flask, jsonify, abort
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
        
app = Flask(__name__)

roadBuffer = 0.0007
client = MongoClient()
db = client.londonDataViz


def toJson(data):
    return json.dumps(data, default=json_util.default)

def getAccidentVehicleStrings(string):
    toReturn = []

    if string=="cycles": toReturn.extend((1,1,1,1))
    if string=="2wheeled": toReturn.extend((2,3,4,5))
    if string=="cars": toReturn.extend((9,9,9,9))
    if string=="buses": toReturn.extend((10,11,11,11))
    if string=="lgvs": toReturn.extend((19,20,20,20))
    if string=="hgvs": toReturn.extend((21,21,21,21))

    return toReturn

@app.route('/accidents/accident_severity=<int:severityNo>', methods=['GET'])
def getBySeverity(severityNo):
    cursor = db.accidents.find({"Accident_Severity": severityNo})
    toReturn = []
    
    for i in cursor:
        toReturn.append(i)
    
    return toJson(toReturn)


@app.route('/accidents/year=<int:year>&accident_severity=<int:severityNo>', methods=['GET'])
def getByAccidentsAndSeverity(year,severityNo):
    
    cursor = db.accidents.find({
        "$and": [
            {"Year":year},
            {"Accident_Severity":severityNo}
            ]
        })
    
    toReturn = []
    
    for i in cursor:
        toReturn.append(i)
    
    return toJson(toReturn)


@app.route('/accidents/year=<int:year>&accident_severity=<int:severityNo>&N=<string:north>&S=<string:south>&E=<string:east>&W=<string:west>', methods=['GET'])
def getByAccidentsAndSeverityWithLatLongConstraints(year,severityNo, north, south, east, west):
    
    cursor = db.accidents.find({
        "$and": [
            {"Year":year},
            {"Accident_Severity":severityNo},
            {"Latitude":{"$lt":float(north)}},
            {"Latitude":{"$gt":float(south)}},
            {"Longitude":{"$lt":float(east)}},
            {"Longitude":{"$gt":float(west)}}
            ]
        })
    
    toReturn = []
    
    for i in cursor:
        toReturn.append(i)
    
    return toJson(toReturn)

@app.route('/accidents/year=<int:year>&accident_severity=<int:severityNo>&vehicle=<string:vehicle>&N=<string:north>&S=<string:south>&E=<string:east>&W=<string:west>', methods=['GET'])
def getByAccidentsAndSeverityWithLatLongConstraintsV(year,severityNo, vehicle, north, south, east, west):
    
    vehicleTypes = getAccidentVehicleStrings(vehicle)

    cursor1 = db.vehicles.find({
        "$or": [
            {"Vehicle_Type": vehicleTypes[0]},
            {"Vehicle_Type": vehicleTypes[1]},
            {"Vehicle_Type": vehicleTypes[2]},
            {"Vehicle_Type": vehicleTypes[3]},
            ]
        })

    accident_id = []

    for i in cursor1:
        accident_id.append(i.get('Accident_Index', ''))

    cursor2 = db.accidents.find({
        "$and": [
            {"Accident_Index": {"$in": accident_id}},
            {"Year":year},
            {"Accident_Severity":severityNo},
            {"Latitude":{"$lt":float(north)}},
            {"Latitude":{"$gt":float(south)}},
            {"Longitude":{"$lt":float(east)}},
            {"Longitude":{"$gt":float(west)}},
            ]
        })
    
    toReturn = []
    
    for i in cursor2:
        toReturn.append(i)

    print toReturn
    
    return toJson(toReturn)

@app.route('/traffic_flow_average_daily/year=<int:year>&N=<string:north>&S=<string:south>&E=<string:east>&W=<string:west>', methods=['GET'])
def getTrafficFlowWithLatLongConstraints(year, north, south, east, west):
    
    cursor = db.traffic_flow_average_daily_byDir.find({
        "$and": [
            {"Year":year},
            {"Latitude":{"$lt":float(north)}},
            {"Latitude":{"$gt":float(south)}},
            {"Longitude":{"$lt":float(east)}},
            {"Longitude":{"$gt":float(west)}}
            ]
        })
    
    toReturn = []

    for i in cursor:
        toReturn.append(i)

    print len(toReturn)
    
    return toJson(toReturn)


@app.route('/charts/accidentsAndFlow/data/chartJS/Lat=<string:latitude>&Lng=<string:longitude>&Dir=<string:Direction>&Linklength=<string:linkLength>', methods=['GET'])
def getChartjsData1(latitude, longitude, Direction, linkLength):
    
    latitude = float(latitude);
    longitude = float(longitude)
    latitudeLower = float(latitude);
    latitudeHigher = float(latitude);
    longitudeLower = float(longitude);
    longitudeHigher = float(longitude);
    radius = (float(linkLength)/120)+roadBuffer;

    if Direction in ("E","W"):
        longitudeLower -=radius
        longitudeHigher +=radius
        latitudeLower -= roadBuffer
        latitudeHigher +=roadBuffer
    elif Direction in ("S","N"):
        longitudeLower -=roadBuffer
        longitudeHigher +=roadBuffer
        latitudeLower -= radius
        latitudeHigher +=radius
    else:
        longitudeLower -=radius
        longitudeHigher +=radius
        latitudeLower -= radius
        latitudeHigher +=radius       

    severityChanges = [[],[],[]]
    flowChange = []

    for i in range(1,4):
        print i
        totalPercentage = 0
        initialVal = db.accidents.count({
            "$and": [
                {"Accident_Severity":i},
                {"Year": 2005},
                {"Latitude":{"$lt":(latitudeHigher)}},
                {"Latitude":{"$gt":(latitudeLower)}},
                {"Longitude":{"$lt":(longitudeHigher)}},
                {"Longitude":{"$gt":(longitudeLower)}}
                ]
            })


        if initialVal == 0:
            severityChanges[i]=[]
        else:
            totalPercentage = 0
            for j in range(2005,2015):
                currentVal = db.accidents.count({
                    "$and": [
                        {"Accident_Severity":i},
                        {"Year":j},
                        {"Latitude":{"$lt":(latitudeHigher)}},
                        {"Latitude":{"$gt":(latitudeLower)}},
                        {"Longitude":{"$lt":(longitudeHigher)}},
                        {"Longitude":{"$gt":(longitudeLower)}}
                        ]
                    })

                totalPercentage += ((currentVal-initialVal)/initialVal)*100
                severityChanges[i-1].append(totalPercentage)

    initialFlow = db.traffic_flow_average_daily_byDir.find({
        "$and": [
            {"Year":2005},
            {"Latitude":latitude},
            {"Longitude":longitude}
            ]
        })[0]["AllMotorVehicles"]

    totalPercentage = 0
    for i in range(2005,2015):
        currentFlow = db.traffic_flow_average_daily_byDir.find({
            "$and": [
                {"Year":i},
                {"Latitude":latitude},
                {"Longitude":longitude}
                ]
            })[0]["AllMotorVehicles"]

        totalPercentage += ((currentFlow-initialFlow)/initialFlow)*100 
        flowChange.append(totalPercentage)
        
    data = toJson({

            "labels":["2005","2006","2007","2008","2009","2010","2011","2012","2013","2014"],

            "datasets": [
                {
                    "label": "severity 3 accidents",
                    "fillColor": "rgba(253, 70, 0, 0.2)",
                    "strokeColor": "rgba(253, 70, 0, 0.9)",
                    "pointColor": "rgba(253, 70, 0, 0.9)",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                    "data": severityChanges[2]
                },
                {
                    "label": "severity 2 accidents",
                    "fillColor": "rgba(253, 126, 43, 0.2)",
                    "strokeColor": "rgba(253, 126, 43, 0.9)",
                    "pointColor": "rgba(253, 126, 43, 0.9)",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                    "data": severityChanges[1]
                },
                {
                    "label": "severity 1 accidents",
                    "fillColor": " rgba(253, 241, 43, 0.2)",
                    "strokeColor": " rgba(253, 241, 43, 0.9)",
                    "pointColor": " rgba(253, 241, 43, 0.9)",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                    "data": severityChanges[0]
                },
                {
                    "label": "flow",
                    "fillColor": "rgba(151,187,205,0.6)",
                    "strokeColor": "rgba(151,187,205,1)",
                    "pointColor": "rgba(151,187,205,1)",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(151,187,205,1)",
                    "data": flowChange
                }
                ]
            })
            
    
    return data

@app.route('/charts/accidents/data/chartJS/Lat=<string:latitude>&Lng=<string:longitude>&Dir=<string:Direction>&Linklength=<string:linkLength>', methods=['GET'])
def getChartjsData2(latitude, longitude, Direction, linkLength):

    latitudeLower = float(latitude);
    latitudeHigher = float(latitude);
    longitudeLower = float(longitude);
    longitudeHigher = float(longitude);
    radius = (float(linkLength)/120)+roadBuffer;

    if Direction in ("E","W"):
        longitudeLower -=radius
        longitudeHigher +=radius
        latitudeLower -= roadBuffer
        latitudeHigher +=roadBuffer
    elif Direction in ("S","N"):
        longitudeLower -=roadBuffer
        longitudeHigher +=roadBuffer
        latitudeLower -= radius
        latitudeHigher +=radius
    else:
        longitudeLower -=radius
        longitudeHigher +=radius
        latitudeLower -= radius
        latitudeHigher +=radius

    severityChanges = [[],[],[]] 

    for i in range(1,4):
            for j in range(2005,2015):
                currentVal = db.accidents.count({
                    "$and": [
                        {"Accident_Severity":i},
                        {"Year":j},
                        {"Latitude":{"$lt":(latitudeHigher)}},
                        {"Latitude":{"$gt":(latitudeLower)}},
                        {"Longitude":{"$lt":(longitudeHigher)}},
                        {"Longitude":{"$gt":(longitudeLower)}}
                        ]
                    })

                severityChanges[i-1].append(currentVal)


    data = toJson({

            "labels":["2005","2006","2007","2008","2009","2010","2011","2012","2013","2014"],

            "datasets": [
                {
                    "label": "severity 3 accidents",
                    "fillColor": "rgba(253, 70, 0, 0.2)",
                    "strokeColor": "rgba(253, 70, 0, 0.9)",
                    "pointColor": "rgba(253, 70, 0, 0.9)",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                    "data": severityChanges[2]
                },
                {
                    "label": "severity 2 accidents",
                    "fillColor": "rgba(253, 126, 43, 0.2)",
                    "strokeColor": "rgba(253, 126, 43, 0.9)",
                    "pointColor": "rgba(253, 126, 43, 0.9)",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                    "data": severityChanges[1]
                },
                {
                    "label": "severity 1 accidents",
                    "fillColor": " rgba(253, 241, 43, 0.2)",
                    "strokeColor": " rgba(253, 241, 43, 0.9)",
                    "pointColor": " rgba(253, 241, 43, 0.9)",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                    "data": severityChanges[0]
                }
                ]
            })
            
    
    return data

@app.route('/charts/accidentsAgainstFlow/data/chartJS/Lat=<string:latitude>&Lng=<string:longitude>&Dir=<string:Direction>&Linklength=<string:linkLength>', methods=['GET'])
def getChartjsData11(latitude, longitude, Direction, linkLength):
    
    latitude = float(latitude);
    longitude = float(longitude)
    latitudeLower = float(latitude);
    latitudeHigher = float(latitude);
    longitudeLower = float(longitude);
    longitudeHigher = float(longitude);
    radius = (float(linkLength)/120)+roadBuffer;

    if Direction in ("E","W"):
        longitudeLower -=radius
        longitudeHigher +=radius
        latitudeLower -= roadBuffer
        latitudeHigher +=roadBuffer
    elif Direction in ("S","N"):
        longitudeLower -=roadBuffer
        longitudeHigher +=roadBuffer
        latitudeLower -= radius
        latitudeHigher +=radius
    else:
        longitudeLower -=radius
        longitudeHigher +=radius
        latitudeLower -= radius
        latitudeHigher +=radius

    severityChanges = [] 
    flowChange = []

    for j in range(2005,2015):
        currentVal = db.accidents.count({
            "$and": [
                {"Year":j},
                {"Latitude":{"$lt":(latitudeHigher)}},
                {"Latitude":{"$gt":(latitudeLower)}},
                {"Longitude":{"$lt":(longitudeHigher)}},
                {"Longitude":{"$gt":(longitudeLower)}}
                    ]
            })

        severityChanges.append(currentVal)

    for i in range(2005,2015):
        currentFlow = db.traffic_flow_average_daily_byDir.find({
            "$and": [
                {"Year":i},
                {"Latitude":latitude},
                {"Longitude":longitude}
                ]
            })[0]["AllMotorVehicles"]

        flowChange.append(currentFlow)
    radiuses = flowRadius(flowChange)
    print radiuses
        
    data = toJson(

                                [
                                    {
                                      "label": ' dataset',
                                      "strokeColor": '##00ffffff.',
                                      "pointColor": '#13a300',
                                      "data": [
                                        { "x": flowChange[0], "y": severityChanges[0] }, 
                                        { "x": flowChange[1], "y": severityChanges[1] }, 
                                        { "x": flowChange[2], "y": severityChanges[2] }, 
                                        { "x": flowChange[3], "y": severityChanges[3] },
                                        { "x": flowChange[4], "y": severityChanges[4] },
                                        { "x": flowChange[5], "y": severityChanges[5] }, 
                                        { "x": flowChange[6], "y": severityChanges[6] },
                                        { "x": flowChange[7], "y": severityChanges[7] },
                                        { "x": flowChange[8], "y": severityChanges[8] },
                                        { "x": flowChange[9], "y": severityChanges[9] }
                                        
                                              ]
                                    }
                                ]
            )
            
    
    return data

def flowRadius(flowChange):
    toReturn = []
    for flow in flowChange:
        if flow==max(flowChange):
           toReturn.append(3.5)
        else:
            toReturn.append((flow/(max(flowChange))*3.5))
    return toReturn
    

@app.route('/charts/flow/data/chartJS/Lat=<string:latitude>&Lng=<string:longitude>', methods=['GET'])
def getChartjsData3(latitude, longitude):
    
    latitude = float(latitude);
    longitude = float(longitude)
    flowChange = []

    for i in range(2005,2015):
        currentFlow = db.traffic_flow_average_daily_byDir.find({
            "$and": [
                {"Year":i},
                {"Latitude":latitude},
                {"Longitude":longitude}
                ]
            })[0]["AllMotorVehicles"]

        flowChange.append(currentFlow)
        
    data = toJson({

            "labels":["2005","2006","2007","2008","2009","2010","2011","2012","2013","2014"],

            "datasets": [
                {
                    "label": "flow",
                    "fillColor": "rgba(151,187,205,0.6)",
                    "strokeColor": "rgba(151,187,205,1)",
                    "pointColor": "rgba(151,187,205,1)",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(151,187,205,1)",
                    "data": flowChange
                }
                ]
            })
            
    
    return data

if __name__ == '__main__':
    app.run(debug=True)

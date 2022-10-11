from flask import Flask, render_template, request
from fileread import data_dict, fare_dict
import function
import datastore
import math
import sqlite3

"""
=================DICTIONARIES DUMP SECTION============================
"""
bus_routes = data_dict('bus_routes.json')
bus_services = data_dict('bus_services.json')
bus_stops = data_dict('bus_stops.json')

"""
===================FLASK CODE DUMP SECTION===========================
"""

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/nearestbus')
def nearestbus():
    if "long" in request.args and "latt" in request.args:
        latt = request.args["latt"]
        long = request.args["long"]
        data = function.nearest_bus_stop(latt, long)
        print(data)
        return render_template('nearestbus.html',data=data)

@app.route('/fare')
def fare():
    if "busno" in request.args and "payment" in request.args and "status" in request.args and "start" in request.args and "end" in request.args:
        busno = request.args["busno"]
        status = request.args["status"]
        payment = request.args["payment"]
        start = request.args["start"]
        end = request.args["end"]

        dist, direction = function.fare_dist(busno, start, end)

        price = function.fares(busno,status, payment, dist, direction)
        if int(price) >= 100:
            price = str(price)
            price = price[:-2]+'.'+price[-2:]
        else:
            price = '0.'+str(price)

        return render_template('fare.html', busno=busno, payment=payment, status=status, start=start, end=end, price=price)


app.run('0.0.0.0')


"""
==================DATABASE DUMP SECTION=============================
"""
# conn = datastore.get_conn()
# cur = conn.cursor()
# datastore.insert_route(bus_routes)
# datastore.insert_service(bus_services)
# datastore.insert_stops(bus_stops)
# conn.commit()
# conn.close()


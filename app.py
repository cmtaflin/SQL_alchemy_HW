#Dependencies

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

##############################################
#           Set-up Database                  #
##############################################

Engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Create based object for data 
Base=automap_base()
#Prepare the data
Base.prepare (Engine, reflect=True)

#Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

#create session (link) from DB to Phython
session= Session (Engine)

##############################################
#                    Flask                   #
##############################################

#Create app
app = Flask(__name__)

##############################################
#                 Flask Routes               #
##############################################

#  start_date= "2015-03-01"
#  end_date= "2015-04-01"

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"


@app.route("/api/v1.0/precipitation")
def precipitation():

    ###Return dictionaries in the format of Json for further analysis
   #1.) Query Data
   #2.) Convert Query-> dictionary
   #3.) convert Dictionary to Json using Jsonfiy

    #Query all data into an an Var object= results
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()

    #Convert query (Object) to dictionary
    precipitation_data=[]
    for precip_data in prcp_results:
        pricip_dict={}
        pricip_dict["date"]=precip_data.date
        pricip_dict["prcp"]=precip_data.prcp
        precipitation_data.append(pricip_dict)
    
    #convert to json
    return jsonify (precipitation_data)

@app.route("/api/v1.0/stations")
def station():

   ###Return dictionaries in the format of Json for further analysis
   #1.) Query Data
   #2.) Convert Query-> dictionary
   #3.) convert Dictionary to Json using Jsonfiy
   
    #Query all data into an an Var object= results
    station_results=session.query((Measurement.station), func.count(Measurement.station)).\
                    group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).all()

    #Convert query (Object) to dictionary
    station_data=[]
    for station_rows in station_results:
        station_dict={}
        station_dict["station"]=station_rows[0]
        station_dict["count"]=station_rows[1]
        station_data.append(station_dict)
    
    #convert to json
    return jsonify (station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    ### from Jupyter file: find 1 year from last date and convert 
    
    #1.) Find last date of data
    last_date=session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()
    
    #2.) for loop to split date data type text into three different properties
    for date in last_date:
       split_last_date=date.split("-")

    #3.) take last date into 3 variables
    last_year=int(split_last_date [0])
    last_month=int(split_last_date [1])
    last_day=int(split_last_date [2])

    #Find Date one year ago
    yr1_ago_date=dt.date(last_year,last_month,last_day)-dt.timedelta(days=365)   


   ###Return dictionaries in the format of Json for further analysis
   #1.) Query Data
   #2.) Convert Query-> dictionary
   #3.) convert Dictionary to Json using Jsonfiy
    
   #Query all data into an an Var object= results
    tobs_results=session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= yr1_ago_date).\
                order_by(Measurement.date).all()
    
    #Convert query (Object) to dictionary
    last_12mnth_tobs_data=[]
    for tobs_rows in tobs_results:
        tobs_dict={}
        tobs_dict["date"]=tobs_rows.date
        tobs_dict["tobs"]=tobs_rows.tobs
        last_12mnth_tobs_data.append(tobs_dict)
     
    #convert to json
    return jsonify (last_12mnth_tobs_data)

# #Below: doesn't work  ####

# @app.route("/api/v1.0/<start>")
# def derive_start_date_temp(start_date):
#     '''TMIN, TAVG, and TMAX for a list of dates
#     Args:
#         start_date(string): A date in the format %Y-%m-%d
#         end_date(string): A date in the format %Y-%m-%d

#     Returns:
#         TMIN, TAVG, and TMAXX'''

#     ###Return dictionaries in the format of Json for further analysis
#     #1.) Query Data
#     #2.) Convert Query-> dictionary
#     #3.) convert Dictionary to Json using Jsonfiy
    
#     #Query all data into an an Var object= results
#     start_results=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
#                   filter(Measurement.date >= start_date).all()
    
#     #Convert query (Object) to dictionary
#     start_results_data=[]
#     for start_result_rows in start_results:
#        start_results_dict={}
#        start_results_dict["Min_tobs"]=start_result_rows[0]
#        start_results_dict["Avg_tobs"]=start_result_rows[1]
#        start_results_dict["Max_tobs"]=start_result_rows[2]
#        start_results_data.append(start_results_dict)

#     #convert to json
#     return jsonify (start_results_data)

# #Below: doesn't work  ####
# @app.route("/api/v1.0/<start>/<end>")
# def derive_start_end_date_temp(end_date):
#     """TMIN, TAVG, and TMAX for a list of dates
#     Args:
#         start_date(string): A date in the format %Y-%m-%d
#         end_date(string): A date in the format %Y-%m-%d

#     Returns:
#         TMIN, TAVG, and TMAXX"""

#     ###Return dictionaries in the format of Json for further analysis
#    #1.) Query Data
#    #2.) Convert Query-> dictionary
#    #3.) convert Dictionary to Json using Jsonfiy
    
#    #Query all data into an an Var object= results
#     start_results=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
#                   filter(Measurement.date>=start_date).\
#                   filter(Measurement.date<=end_date).all()
    
#    #Convert query (Object) to dictionary
#     start_results_data=[]
#     for start_result_rows in start_results:
#        start_results_dict={}
#        start_results_dict["Min_tobs"]= start_result_rows[0]
#        start_results_dict["Avg_tobs"]= start_result_rows[1]
#        start_results_dict["Max_tobs"]= start_result_rows[2]
#        start_results_data.append(start_results_dict)

#     #convert to json
#     return jsonify (start_results_data)

if __name__ == "__main__":
    app.run(debug=True)
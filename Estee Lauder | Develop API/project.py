# Write a web API that returns a set of food trucks. 
# Write a web frontend that visualizes the nearby food trucks for a given place. 
# Create a CLI that lets us get the names of all the taco trucks in the city. 
# Create system that spits out a container with a placeholder webpage featuring the name of each food truck to help their marketing efforts.

#  San Francisco's food truck open dataset is https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat/data


import requests
import flask
from flask import Flask, render_template, request, redirect, url_for
import csv

class FoodTruck:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

app = flask.Flask(__name__,template_folder='templates')
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])

def home(): # home page
    return render_template('index.html')

# get food trucks from api
def get_food_trucks():
    food_trucks = []
    r = requests.get('https://data.sfgov.org/resource/rqzj-sfat.json')

    for truck in r.json():
        food_trucks.append(FoodTruck(truck['applicant'], truck['latitude'], truck['longitude']))
    return food_trucks

# get food trucks names and locations
def get_food_truck_names_and_locations():
    food_trucks = get_food_trucks()
    names = []
    locations = []

    for truck in food_trucks:
        names.append(truck.name)
        locations.append((truck.latitude, truck.longitude))
    return names, locations

# export data to csv
def export_data():
    food_trucks = get_food_trucks()

    with open('trucks.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'latitude', 'longitude'])
        for truck in food_trucks:
            writer.writerow([truck.name, truck.latitude, truck.longitude])

def main():
    export_data()
    app.run()

if __name__ == "__main__":
    main()
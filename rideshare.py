# Author: Dillon Earl Jones (dej0044) (DillonJones@my.unt.edu)
# Assignment: Intro to AI Project 1 - Ride share agent
# Description: A program written only by me to fulfil most if not all requirements of project 1 part B
import random

import networkx as nx
import queue as q
import random as seeder
import tkinter as tk
import sys

# --------------------------- Classes ---------------------------


class Van:
    def __init__(self):
        self.Requests = q.Queue()
        self.Scheduled = q.Queue()
        self.vanID = 0
        self.current_location = 0
        self. dist_to_location = 0
        self.distance_traveled = 0
        self.num_trips = 0
        self.current_path = []
        self.current_request = Request()


class Request:
    def __init__(self):
        self.pickup_location = 0
        self.drop_location = 0


# ----------------------- Greeting -----------------------------
print("Author: Dillon Earl Jones")
print("Email: DillonJones@my.unt.edu")
print("CSCE 5201 Project 1 - Ride Share Agent")

# ------------------------ City Init ---------------------------


seed = seeder.Random()
citySpots = nx.gnp_random_graph(200, 0.4, seed)
print("City Nodes: " + str(citySpots.nodes()))

print("City Edges: " + str(citySpots.edges()))


# -------------------- Init Vans -------------------------------

vans = []

nextID = 0
for i in range(59):
    van = Van()
    nextID += 1
    van.vanID = nextID
    van.current_location = seeder.randint(0, 199)
    vans.append(van)

# ----------------- Requests ----------------------
# 5 Requests are made for testing as if the ride day started with requests before opening
global_requests = q.Queue()

req = Request()
req.pickup_location = 67
req.drop_location = 22
global_requests.put(req)

req2 = Request()
req2.pickup_location = 43
req2.drop_location = 15
global_requests.put(req2)

req3 = Request()
req3.pickup_location = 77
req3.drop_location = 36
global_requests.put(req3)

req4 = Request()
req4.pickup_location = 45
req4.drop_location = 12
global_requests.put(req4)

req5 = Request()
req5.pickup_location = 55
req5.drop_location = 50
global_requests.put(req5)


def generate_requests():
    random_num_reqs = seeder.randint(450, 599)
    for req_rand in range(random_num_reqs):
        new_req = Request()
        new_req.pickup_location = seeder.randint(0, 199)
        new_req.drop_location = seeder.randint(0, 199)
        global_requests.put(new_req)


# Assigns the rides from the global request queue to the vans
def find_closest_van(request):
    print("Current Requested Pickup Loc: " + str(request.pickup_location))
    for index in range(59):
        check_van = vans[index]
        check_van.dist_to_location = nx.astar_path_length(citySpots,
                                                          check_van.current_location, request.pickup_location)

    closest_van = min(vans, key=lambda van: van.dist_to_location)
    print("Closest Van is ID of: " + str(closest_van.vanID) +
          " with current location of: " + str(closest_van.current_location))
    closest_van.Requests.put(request)
    return closest_van


root = tk.Tk()  # Root of the clock to run the simulation


# Logic that drives the agent to fill their request queue
def ride_share():
    print("Hello, follow instructions to enter new requests")
    add_request()
    print("There are currently " + str(global_requests.qsize()) + " requests in the global queue.")
    while global_requests.qsize() != 0:
        cur_req = global_requests.get()
        closest = find_closest_van(cur_req)
    for van_check in vans:
        if not van_check.Requests.empty():
            print("Van ID: " + str(van_check.vanID) + " has " + str(van_check.Requests.qsize()) + " requests.")
    schedule_rides()
    for van_check in vans:
        if van_check.current_path.__len__() != 0:
            print("Van ID: " + str(van_check.vanID) + "; Current Path: " + str(van_check.current_path))
    # move_vans()
    root.after(240000, ride_share)


def schedule_rides():
    print("All Vans are Scheduling Rides")
    for index in range(59):
        check_van = vans[index]
        for index2 in range(check_van.Requests.qsize()):
            if check_van.Requests.empty():
                continue
            else:
                check_van.Scheduled.put(check_van.Requests.get())
        if not check_van.Scheduled.empty():
            print("Rides Scheduled for VanID: " + str(check_van.vanID))
            check_van.current_request = check_van.Scheduled.get()
            check_van.current_path = nx.astar_path(citySpots, check_van.current_location,
                                                   check_van.current_request.pickup_location)


def move_vans():
    print("Moving Vans")
    for van_check in vans:
        if van_check.current_path.__len__() != 0:
            van_check.current_location = van_check.current_path.pop()
            print("Van ID: " + str(van_check.vanID) + " moved to " + str(van_check.current_location))
            if van_check.current_location == van_check.current_request.pickup_location:
                print("Van ID: " + str(van_check.vanID) + " has picked up a passenger.")
                van_check.num_trips += 1
            van_check.distance_traveled += 30
            if len(van_check.current_path) == 0:
                van_check.current_path = nx.astar_path(citySpots, van_check.current_location,
                                                       van_check.current_request.drop_location)
            if van_check.current_location == van_check.current_request.drop_location:
                print("Van ID: " + str(van_check.vanID) + " dropped off a passenger.")
                if not van_check.Scheduled.empty():
                    van_check.current_request = van_check.Scheduled.get()
                    van_check.current_path = nx.astar_path(citySpots, van_check.current_location,
                                                           van_check.current_request.pickup_location)
                    print("Van ID: " + str(van_check.vanID) + "; Next Path: ")
                    for node in van_check.current_path[::]:
                        print(str(node) + ",")
                else:
                    van_check.current_location = van_check.current_location
                    van_check.current_path = []
                    continue
    root.after(500, move_vans)


# 8 hours = 480 minutes = 28800 seconds
# 1 Min = 0.5 seconds

def print_van_distances():
    van_count = 0
    sum_dist = 0
    sum_trips = 0
    for van_check in vans:
        van_count += 1
        print("Van ID: " + str(van_check.vanID) + "; Total Distance Traveled: " +
              str(van_check.distance_traveled) + " miles; Total Trips: " + str(van_check.num_trips))
        sum_dist += van_check.distance_traveled
        sum_trips += van_check.num_trips
    dist_avg = sum_dist / van_count
    trip_avg = sum_trips / van_count
    print("Total Average Distance Traveled of all Vans: " + str(dist_avg) + " miles.")
    print("Total Average Num Trips of all Vans: " + str(trip_avg) + " trips.")


def add_request():
    command = ""
    while command != "start":
        print("Type \"add\" to add a request")
        print("Type \"start\" to start simulation")
        print("Type \"dist\" to print distances")
        print("Type \"close\" to end the program")
        command = input("Command: ")
        if command == "add":
            generate_requests()
        elif command == "dist":
            print_van_distances()
        elif command == "start":
            print("Starting Simulation...")
        elif command == "close":
            sys.exit(1)
        else:
            print("Unknown input, try again.")


root.after(500, ride_share)
root.after(60000, move_vans)

root.mainloop()

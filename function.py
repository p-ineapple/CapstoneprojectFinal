from datastore import DataStore
from fileread import fare_dict

datastore = DataStore('capstone.db')

express = fare_dict('fare_data/fares-for-express-bus-services-effective-from-28-december-2019.csv')
feeder = fare_dict('fare_data/fares-for-feeder-bus-services-effective-from-28-december-2019.csv')
trunk = fare_dict('fare_data/fares-for-trunk-bus-services-effective-from-28-december-2019.csv')


def nearest_bus_stop(lat, long):
    """
    takes in the lattitude and longtitude of the location
    using insertion sort to sort the 5 nearest bus stops
    returns the first 5 nearest bus stops from the point given in a list of tuples containg the bus stop data of each stop
    """
    data = datastore.get_stops()
    dist_sort = []
    dist_data =[]
    for i in range(len(data)):
        lat_dist = float(lat) - data[i][-2]
        long_dist = float(long) - data[i][-1]
        value = long_dist**2 + lat_dist**2
        dist = value**0.5
        if i == 0:
            dist_data.append(dist)
            dist_sort.append(data[i])

        elif dist < dist_data[0]:
            dist_data.insert(0,dist)
            dist_sort.insert(0,data[i])

        else:
            for j in range(len(dist_data)-1):
                
                if dist_data [j] < dist <= dist_data[j+1]:
                    dist_data.insert(j+1,dist)
                    dist_sort.insert(j+1, data[j])
    return dist_sort[:5]

def fare_dist(bus, startcode, endcode):
    """
    takes in the bus service number, starting bus stop code and ending bus stop code
    returns a list containing the distance travelled by the bus and direction of the route
    """
    start_data  = datastore.get_stopsequence(bus, startcode)
    end_data  = datastore.get_stopsequence(bus, endcode)
    stopseq = [start_data[0][0], end_data[0][0], start_data[0][1]]
    all_stops = datastore.get_routes(bus, stopseq[-1], stopseq[0], stopseq[1])
    print(all_stops)
    dist = 0
    for i in range(1, len(all_stops)):
        dist += all_stops[i][5]    
    return dist,start_data[0][1]

def fares(bus, status, payment, dist, direction):
    """
    takes in bus service number, status of the passanger, payment type, distance travelled by bus, and direction of route
    returns the fare of the bus trip in $
    """
    bus_type = datastore.get_bustype(bus, direction)
    bus_type = bus_type[0][0]
    info = [status,payment,'fare_per_ride']
    label = '_'.join(info)
    if bus_type == "TRUNK":
        data  = trunk
    else:
        data = express
    if bus_type == "FEEDER":
        data = feeder
        fare = data[0][label]
    else:
        if dist < 3.2:
            fare = data[0][label]
        elif dist > 40.2:
            fare = data[0][label]
        else:
            for i in range(1, len(data)-1):
                dist_limit = data[i]['distance'].split(' ')
                mini = dist_limit[0]
                maxi = dist_limit[-2]
                if float(mini) <= dist <= float(maxi):
                    num = i
                    break
            fare = data[num][label]
    return fare


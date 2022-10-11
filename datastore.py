import sqlite3

SQL = {
    'bus_routes_table':'''
    CREATE TABLE IF NOT EXISTS "bus_routes"(
        "ServiceNo" INTEGER,
        "Operator" TEXT,
        "Direction" INTEGER,
        "StopSequence" INTEGER,
        "BusStopCode" INTEGER,
        "Distance" INTEGER,
        "WD_FirstBus" INTEGER,
        "WD_LastBus" INTEGER,
        "SAT_FirstBus" INTEGER,
        "SAT_LastBus" INTEGER,
        "SUN_FirstBus" INTEGER,
        "SUN_LastBus" INTEGER,
        PRIMARY KEY ('ServiceNo','Direction','StopSequence')
        FOREIGN KEY(ServiceNo) REFERENCES bus_service(ServiceNo),
        FOREIGN KEY(BusStopCode) REFERENCES bus_stops(BusStopCode));
    ''',

    'bus_services_table':'''
    CREATE TABLE IF NOT EXISTS "bus_services"(
        "ServiceNo" INTEGER,
        "Operator" TEXT,
        "Direction" INTEGER,
        "Category" TEXT,
        "OriginCode" INTEGER,
        "DestinationCode" INTEGER,
        "AM_Peak_Freq" TEXT,
        "AM_Offpeak_Freq" TEXT,
        "PM_Peak_Freq" TEXT,
        "PM_Offpeak_Freq" TEXT,
        "LoopDesc" TEXT,
        PRIMARY KEY('ServiceNo','Direction','DestinationCode'));
    ''',

    'bus_stops_table':'''
    CREATE TABLE IF NOT EXISTS "bus_stops"(
        "BusStopCode" INTEGER,
        "RoadName" TEXT,
        "Description" TEXT,
        "Latitude" REAL,
        "Longitude" REAL,
        PRIMARY KEY(BusStopCode));
    ''',

    'insert_route':'''
    INSERT INTO bus_routes("ServiceNo","Operator","Direction","StopSequence","BusStopCode","Distance","WD_FirstBus","WD_LastBus","SAT_FirstBus","SAT_LastBus","SUN_FirstBus","SUN_LastBus")
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?);
    ''',

    'insert_service':'''
    INSERT INTO bus_services("ServiceNo","Operator","Direction","Category","OriginCode","DestinationCode","AM_Peak_Freq","AM_Offpeak_Freq","PM_Peak_Freq","PM_Offpeak_Freq","LoopDesc")
    VALUES(?,?,?,?,?,?,?,?,?,?,?);
    ''',

    'insert_stops':'''
    INSERT INTO bus_stops("BusStopCode","RoadName","Description","Latitude","Longitude")
    VALUES(?,?,?,?,?);
    ''',

    'get_stopsequence':
    '''
    SELECT StopSequence, Direction
    FROM bus_routes
    WHERE ServiceNo = ? AND BusStopCode = ?;
    ''',
    
    'get_routes': '''
    SELECT * FROM bus_routes
    WHERE ServiceNo = ? AND Direction = ? AND StopSequence >= ? AND StopSequence <= ?;
    ''',

    'get_bustype':'''
    SELECT Category
    FROM bus_services
    WHERE ServiceNo = ? AND Direction = ? ;
    ''',

    'get_stops':'''
    SELECT * FROM bus_stops;
    ''',
    }


'''capstone.db'''
class Connect:
    
    def __init__(self, uri):
        self.uri = uri

    def get_conn(self):
        """
        connects to the db sql file
        """
        self.conn = sqlite3.connect(self.uri)
        self.cur = self.conn.cursor()
        return self.conn, self.cur


class DataStore(Connect):

    def get_stopsequence(self, serviceno, buscode):
        """
        takes in bus service number and bus stop code
        returns a list containing a tuple of stop sequence and bus direction
        """
        conn, cur  = self.get_conn()
        cur.execute(SQL['get_stopsequence'], (serviceno, buscode))
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data

    def get_routes(self, serviceno, direction, startno, endno):
        """
        takes in bus service number, direction, start stopsequence, end stopsequence
        returns a list of tuples, which contains the data of bus routes passes by from the start sequence to the end sequence
        """
        conn, cur  = self.get_conn()
        cur.execute(SQL['get_routes'], (serviceno, direction, startno, endno))
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data
        
    def get_bustype(self, serviceno, direction):
        """
        takes in bus service number and direction
        returns a tuple containg the bus' category
        """
        conn, cur  = self.get_conn()
        cur.execute(SQL['get_bustype'], (serviceno,direction))
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data

    def get_stops(self):
        """
        returns a list of tuples containing all bus stop data
        """
        conn, cur  = self.get_conn()
        cur.execute(SQL['get_stops'])
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data


'''
===========IMPLEMENTING DATABASE CODE DUMP SECTION====================
'''

# def insert_route(data):
#     '''
#     creates a bus_routes table
#     inputs data into the table
#     '''
#     conn = get_conn()
#     cur = conn.cursor()
#     cur.execute(SQL['bus_routes_table']);
#     for entry in data:
#         values = entry.values()
#         cur.execute(SQL['insert_route'],list(values))
#     conn.commit()
#     conn.close()
        

# def insert_service(data):
#     '''
#     creates a bus_service table
#     inputs data into the table
#     '''
#     conn = get_conn()
#     cur = conn.cursor()
#     cur.execute(SQL['bus_services_table']);
#     for entry in data:
#         values = entry.values()
#         cur.execute(SQL['insert_service'],list(values))
#     conn.commit()
#     conn.close()
        

# def insert_stops(data):
#     '''
#     creates a bus_stops table
#     inputs data into the table
#     '''
#     conn = get_conn()
#     cur = conn.cursor()
#     cur.execute(SQL['bus_stops_table']);
#     for entry in data:
#         values = entry.values()
#         cur.execute(SQL['insert_stops'],list(values))
#     conn.commit()
#     conn.close()
        
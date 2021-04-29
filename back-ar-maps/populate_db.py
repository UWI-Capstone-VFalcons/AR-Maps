from app import db
from app.models import *

# add default buildings
 
b1 = Building(
    name='Science and Technology Library',
    address1="2742+46", 
    address2="Kingston, Jamaica", 
    b_type="Library", 
    info="The main Library of the Sci- Tech faculty",
    latitude=18.005339,
    longitude=-76.749472)

b2 = Building(
    name='Science Lecture Theatre 2',
    address1="2742+34", 
    address2="Kingston, Jamaica", 
    b_type="Lecture Theatre", 
    info="SLT 2",
    latitude=18.005164,
    longitude=-76.749748)

b3 = Building(
    name='Science Lecture Theatre 1',
    address1="2742+32", 
    address2="Kingston, Jamaica", 
    b_type="Lecture Theatre", 
    info="SLT 1",
    latitude=18.005172,
    longitude=-76.749948)

b4 = Building(
    name='Science and Technology Faculty Office',
    address1="2742+32", 
    address2="Kingston, Jamaica", 
    b_type="Lecture Theatre", 
    info="The faculty office and Deans office ",
    latitude=18.005356,
    longitude=-76.749883)

b5 = Building(
    name='Aunty Jackie\'s Shop',
    address1="2742+24", 
    address2="Kingston, Jamaica", 
    b_type="Stall", 
    info="Aunty Jackie\'s Food and Supplies Shop",
    latitude=18.005061,
    longitude=-76.749630)

db.session.add(b1)
db.session.add(b2)
db.session.add(b3)
db.session.add(b4)
db.session.add(b5)

# commit the insertions to the database
db.session.commit()

# add events

# Add Map Area
ma1 = MapArea(
    name="Science & Technology Faculty",
    description="The science faculty of the Universiy of the west Indies",
    latitude_1= 18.003364,
    longitude_1= -76.749843,
    latitude_2= 18.005778,
    longitude_2= -76.751507, 
    latitude_3= 18.006836,
    longitude_3= -76.749104,
    latitude_4= 18.004963,
    longitude_4= -76.748221)

db.session.add(ma1)

# commit the insertions to the database
db.session.commit()

# add Map Zones
mz1 = MapZone(
    name="Zone A",
    map_area=1,
    latitude_1= 18.005706,
    longitude_1= -76.748579,
    latitude_2= 18.005494,
    longitude_2= -76.748539 ,
    latitude_3= 18.005327,
    longitude_3= -76.748749,
    latitude_4= 18.005529284218035,
    longitude_4=-76.74892187118532)

mz2 = MapZone(
    name="Zone B",
    map_area=1,
    latitude_1= 18.005529284218035,
    longitude_1=-76.74892187118532,
    latitude_2= 18.005327,
    longitude_2= -76.748749,
    latitude_3= 18.005167062810408,
    longitude_3= -76.74905598163606 ,
    latitude_4= 18.005406843262104,
    longitude_4= -76.74925446510316)

mz3 = MapZone(
    name="Zone C",
    map_area=1,
    latitude_1= 18.005406843262104,
    longitude_1= -76.74925446510316,
    latitude_2= 18.005167062810408,
    longitude_2= -76.74905598163606,
    latitude_3= 18.005065,
    longitude_3= -76.749454,
    latitude_4= 18.00524358852193,
    longitude_4= -76.74952805042268)

mz4 = MapZone(
    name="Zone D",
    map_area=1,
    latitude_1= 18.00524358852193,
    longitude_1= -76.74952805042268,
    latitude_2= 18.005065,
    longitude_2= -76.749454,
    latitude_3= 18.004976,
    longitude_3= -76.749713,
    latitude_4= 18.005110943934206,
    longitude_4= -76.74973189830781)

db.session.add(mz1)
db.session.add(mz2)
db.session.add(mz3)
db.session.add(mz4)

# commit the insertions to the database
db.session.commit()

# add nodes
n1 = Node(
    latitude_1=18.005667,
    longitude_1=-76.748556,
    latitude_2= 18.005619,
    longitude_2= -76.748535,
    description= "sci-tech entrance")

n2 = Node(
    latitude_1=18.005377,
    longitude_1= -76.749178,
    latitude_2= 18.005335,
    longitude_2= -76.749152,
    description= "sci-tech entrance")

n3 = Node(
    latitude_1=18.005046,
    longitude_1=-76.749713,
    latitude_2= 18.005015,
    longitude_2= -76.749696,
    description= "Miss.Jackie Stall")  

n4 = Node(
    latitude_1=18.005075,
    longitude_1=-76.749651,
    latitude_2= 18.005029,
    longitude_2= -76.749608,
    description= "Miss.Jackie Stall")  

n4 = Node(
    latitude_1=18.005482,
    longitude_1=-76.749959,
    latitude_2= 18.005465,
    longitude_2= -76.750019,
    description= "Faculty Office")  

n5 = Node(
    latitude_1=18.004602,
    longitude_1=-76.749443,
    latitude_2= 18.004588,
    longitude_2= -76.749468,
    description= "Mathematics department")  

n6 = Node(
    latitude_1=18.005218079955107,
    longitude_1=-76.7494583129883,
    latitude_2= 18.00519767309901,
    longitude_2= -76.74942612648012,
    description= "Sci-Tech Library stop point")  

n7 = Node(
    latitude_1=18.00510074050024,
    longitude_1=-76.74967959523202,
    latitude_2= 18.005075231912745,
    longitude_2= -76.74965411424638,
    description= "Sci-Tech SLT2 stop point")  

n8 = Node(
    latitude_1= 18.00522063081196,
    longitude_1=-76.74983248114586,
    latitude_2= 18.005205,
    longitude_2=-76.749876,
    description= "Sci-Tech SLT1 stop point")

n9 = Node(
    latitude_1=18.005349449034735,
    longitude_1= -76.7499089241028,
    latitude_2= 18.005341,
    longitude_2= -76.749938,
    description= "Sci-Tech Main Office stop point")    

db.session.add(n1)
db.session.add(n2)
db.session.add(n3)
db.session.add(n4)
db.session.add(n5)
db.session.add(n6)
db.session.add(n7)
db.session.add(n8)
db.session.add(n9)


# commit the insertions to the database
db.session.commit()

# add paths
p1 = Path(
    name="sci-tech Juici Patty entrance",
    start=1,
    end=2,
    map_area=1)

p2 = Path(
    name="sci-tech library",
    start=2,
    end=3,
    map_area=1)

p3 = Path(
    name="sci-tech faculty office",
    start=3,
    end=4,
    map_area=1)

p4 = Path(
    name="sci-tech mathematics department",
    start=3,
    end=5,
    map_area=1)

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)

# commit the insertions to the database
db.session.commit()

# add path connections
pc1 = Path_Connection(
    path1=1,
    path2=2)

pc2 = Path_Connection(
    path1=2,
    path2=3)

pc3 = Path_Connection(
    path1=2,
    path2=4)

db.session.add(pc1)
db.session.add(pc2)
db.session.add(pc3)

# commit the insertions to the database
db.session.commit()


# add path building connection

pbc1 = Path_Building_Connection(
    building_id=1,
    path=2,
    stop_node=6)

pbc2 = Path_Building_Connection(
    building_id=2,
    path=2,
    stop_node=7)

pbc3 = Path_Building_Connection(
    building_id=3,
    path=3,
    stop_node=8)

pbc4 = Path_Building_Connection(
    building_id=4,
    path=3,
    stop_node=9)

db.session.add(pbc1)
db.session.add(pbc2)
db.session.add(pbc3)
db.session.add(pbc4)


# commit the insertions to the database
db.session.commit()

# Add starting points
sp = Starting_Point(
    name= "Juici Patty Entrance", 
    latitude= 18.005642, 
    longitude= -76.748532)

db.session.add(sp)

# commit the insertions to the database
db.session.commit()

# add OD objects
odo1 = OD_Objects(
    name="Aunty Jackie Stall", 
    object_name="18.0050609_-76.7496662_auntyjackie", 
    map_zone=4,
    latitude=18.0050609, 
    longitude=-76.7496662)

odo2 = OD_Objects(
    name="Aunty Jackie Bench", 
    object_name="18.0050864_-76.7496363_bench", 
    map_zone=4,
    latitude=18.0050864, 
    longitude=-76.7496363)

odo3 = OD_Objects(
    name="Sci-Tech Library Stall", 
    object_name="18.0051667_-76.74944412_librarystall", 
    map_zone=3,
    latitude=18.0051667, 
    longitude=-76.74944412)

odo4 = OD_Objects(
    name="Science Lecture Theatre 1 Door", 
    object_name="18.0051836_-76.7497262_pclt1", 
    building_id=3,
    latitude=18.0051836, 
    longitude=-76.7497262)

odo5 = OD_Objects(
    name="Sci-Tech entrance recycle bin", 
    object_name="18.0053245_-76.7486424_recyclebin", 
    map_zone=1,
    latitude=18.0053245, 
    longitude=-76.7486424)

odo6 = OD_Objects(
    name="Sci-Tech entrance Sign", 
    object_name="18.0053530_-76.7490375_signatentrancetoscitech", 
    map_zone=1,
    latitude=18.0053530, 
    longitude=-76.7490375)

odo7 = OD_Objects(
    name="Sci-Tech Library Sign", 
    object_name="18.0053644_-76.7493880_librarysign", 
    map_zone=3,
    latitude=18.0053644, 
    longitude=-76.7493880)

odo8 = OD_Objects(
    name="Sci-Tech Physics Department Sign", 
    object_name="18.0053657_-76.7491452_physicssign", 
    map_zone=2,
    latitude=18.0053657, 
    longitude=-76.7491452)

odo9 = OD_Objects(
    name="Sci-Tech blue sign", 
    object_name="18.0055634_-76.7484079_scitechsign", 
    map_zone=2,
    latitude=18.0055634, 
    longitude=-76.7484079)

db.session.add(odo1)
db.session.add(odo2)
db.session.add(odo3)
db.session.add(odo4)
db.session.add(odo5)
db.session.add(odo6)
db.session.add(odo7)
db.session.add(odo8)
db.session.add(odo9)

# commit the insertions to the database
db.session.commit()
# from app import db
from math import dist
from app.helper import *
from app.views import *
from app.database_object_modifiers import *

if __name__ == '__main__':
   # a = checkCurrentAndDestination((18.005019529041988, -76.74933235613977), 1)
   # building = Building.query.get(1)
   # dest_coord = (float(building.latitude),float(building.longitude))
   # a = estimateDistanceAndTime(
   #    (18.00520017651841,-76.74941982751545), 
   #    dest_coord, 
   #    (18.00561828188547, -76.748552446822),
   #    [])
   # b = dist(
   #    (18.002903738473425, -76.74732416609262),
   #    (17.999546906527225, -76.74373170926685))

   # c = get_shortest_path_overhead(18.00520017651841,-76.74941982751545, 1)
   # print(a)
   # print(b)
   # print(c)
   # addPath(
   #    name="Test4",
   #    map_area_id=1,
   #    connected_path=1,
   #    use_connected_path_end_for_start=True,
   #    end_node_coord1=(18.002903738473425, -76.74732416609262),
   #    end_node_coord2=(18.002903738473425, -76.74732416609262))
   addEvent(
      building_id=1,
      name="edsds")
      

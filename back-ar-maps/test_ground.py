# from app import db
from app.helper import *
from app.views import *

if __name__ == '__main__':
   testBuilding = Building.query.get(3)
   a = generateShortestRoute(1, testBuilding ,1)
   print(a)
   postLengths(1)

# from app import db
from app.helper import *
from app.views import *

if __name__ == '__main__':
   sp = Starting_Point.query.get(1)
   a = estimateDistanceAndTime((18.005151, -76.749463),(1,2),sp, [1,2,3])
   print(a)

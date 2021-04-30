# from app import db
from app.helper import *
from app.views import *

if __name__ == '__main__':
   a = generateShortestRoute(1,3,1)
   print(a)

   b = shortestRoute((18.005653, -76.748327),4)
   print(b)

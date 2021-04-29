# from app import db
from app.helper import *
from app.views import *

if __name__ == '__main__':
   a = closestStartingPoint((18.006684, -76.749459), 1,1)
   print(a)
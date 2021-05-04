# from app import db
from app.helper import *
from app.views import *

if __name__ == '__main__':
#    a = generateShortestRoute(1,3,1)
#    print(a)

#    b = shortestRoute((18.005653, -76.748327),4)
#    print(b)

    c = getPositions([(18.005667, -76.748556),(18.005619, -76.748535)],[(18.005377,-76.749178), (18.005335, -76.749152)])
    print([(18.005667, -76.748556),(18.005619, -76.748535)],[(18.005377,-76.749178), (18.005335, -76.749152)])
    print(c)
   sp = Starting_Point.query.get(1)
   a = estimateDistanceAndTime((18.005151, -76.749463),(1,2),sp, [1,2,3])
   print(a)

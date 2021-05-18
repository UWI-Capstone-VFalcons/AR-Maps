from app.database_object_modifiers import *

"""
This file contains the objects required
for the science and technology region 

Note:
    - all the coordinates are written in a clockwise direction relative to the normal walking direction 
    with the person looking backwards, assume the person never turn back or walk backwards
    - the path nodes are treated separately, the start node is parallel to the end node
"""

"""
add the map area
"""
addMapArea(
    name="Science & Technology Faculty",
    description="The science faculty of the Universiy of the west Indies",
    coord_1=(18.003364, -76.749843),
    coord_2=(18.005778, -76.751507),
    coord_3=(18.006836, -76.749104),
    coord_4=(18.004963, -76.748221))

"""
add all the map zones
"""
addMapZone(
    name="Zone A",
    map_area=1,
    coord_1=(18.005706, -76.748579),
    coord_2=(18.005494, -76.748539),
    coord_3=(18.005327, -76.748749),
    coord_4=(18.005529284218035, -76.74892187118532))

addMapZone(
    name="Zone B",
    map_area=1,
    coord_1=(18.005529284218035, -76.74892187118532),
    coord_2=(18.005327, -76.748749),
    coord_3=(18.005167062810408, -76.74905598163606),
    coord_4=(18.005406843262104, -76.74925446510316))

addMapZone(
    name="Zone C",
    map_area=1,
    coord_1=(18.005406843262104, -76.74925446510316),
    coord_2=(18.005167062810408,-76.74905598163606),
    coord_3=(18.005065, -76.749454),
    coord_4=(18.00524358852193, -76.74952805042268))

addMapZone(
    name="Zone D",
    map_area=1,
    coord_1=(18.00524358852193, -76.74952805042268),
    coord_2=(18.005065, -76.749454),
    coord_3=(18.004976, -76.749713),
    coord_4=(18.005110943934206, -76.74973189830781))

"""
add all the paths
"""
# starting from juici patty entrance
addPath(
    name="sci-tech Juici Patty entrance",
    start_node_coord1=(18.005667, -76.748556),
    start_node_coord2=(18.005619, -76.748535),
    end_node_coord1=(18.005377, -76.749178),
    end_node_coord2=(18.005335, -76.749152),
    connected_path=None,
    use_connected_path_end_for_start=False,
    map_area_id=1)

addPath(
    name="Physics Department entrance",
    start_node_coord1=(),
    start_node_coord2=(),
    end_node_coord1=(18.00534861396561, -76.74924253963613),
    end_node_coord2=(18.005307661780623, -76.74921144001362),
    use_connected_path_end_for_start=True,
    connected_path=1,
    map_area_id=1)

addPath(
    name="sci-tech library",
    start_node_coord1=(),
    start_node_coord2=(),
    end_node_coord1=(18.00521679908835, -76.74943779441655),
    end_node_coord2=(18.005186042763917, -76.74941744180083),
    use_connected_path_end_for_start=True,
    connected_path=2,
    map_area_id=1)

addPath(
    name="Aunty Jackie",
    start_node_coord1=(),
    start_node_coord2=(),
    end_node_coord1=(18.00510010578228, -76.74965988096477),
    end_node_coord2=(18.00504159274003, -76.74963732429521),
    use_connected_path_end_for_start=True,
    connected_path=3,
    map_area_id=1)

# intersection at aunty jackie
# moving towards the chemistry department
addPath(
    name="Sci-tech Spine",
    start_node_coord1=(),
    start_node_coord2=(),
    end_node_coord1=(18.005036441843345, -76.74978670556446),
    end_node_coord2=(18.004993157552466, -76.74975459267655),
    use_connected_path_end_for_start=True,
    connected_path=4,
    map_area_id=1)

addPath(
    name="Mathematics Department",
    start_node_coord1=(18.005014849567072, -76.74977007123917),
    start_node_coord2=(18.00503580066289, -76.74973496572754),
    end_node_coord1=(18.00485825002718, -76.74968062829494),
    end_node_coord2=(18.004881203254378, -76.74962039334395),
    use_connected_path_end_for_start=False,
    connected_path=5,
    map_area_id=1)

addPath(
    name="Sci-Tech Spine",
    start_node_coord1=(),
    start_node_coord2=(),
    end_node_coord1=(18.004718275960492, -76.74958295778654),
    end_node_coord2=(18.0047571134983, -76.74952050406634),
    use_connected_path_end_for_start=True,
    connected_path=6,
    map_area_id=1)

addPath(
    name="sci-tech chemistry entrance",
    start_node_coord1=(),
    start_node_coord2=(),
    end_node_coord1=(18.00451030264787, -76.74941405557355),
    end_node_coord2=(18.00454906360535, -76.74936412829803),
    use_connected_path_end_for_start=True,
    connected_path=7,
    map_area_id=1)

addPath(
    name="sci-tech chemistry entrance",
    start_node_coord1=(18.00458015350089, -76.74939350132085),
    start_node_coord2=(18.004560447579127, -76.7493491571364),
    end_node_coord1=(18.004449224951777, -76.74952693395014),
    end_node_coord2=(18.00441588039336, -76.74947434213577),
    use_connected_path_end_for_start=False,
    connected_path=8,
    map_area_id=1)

# moving from auty jackie intersecion to the faculty office
addPath(
    name="Spine SLT 2 ",
    start_node_coord1=(18.005031169137617, -76.74973650055414),
    start_node_coord2=(18.005008833049494, -76.74977676052885),
    end_node_coord1=(18.005099289560107, -76.74977455642524),
    end_node_coord2=(18.005094221678775, -76.74981051838598),
    use_connected_path_end_for_start=False,
    connected_path=5,
    map_area_id=1)

addPath(
    name="Spine SLT 1",
    start_node_coord1=(),
    start_node_coord2=(),
    end_node_coord1=(18.005203792323844, -76.74981844034289),
    end_node_coord2=(18.005181561801386, -76.74985817833058),
    use_connected_path_end_for_start=True,
    connected_path=10,
    map_area_id=1)

addPath(
    name="sci-tech faculty office",
    start_node_coord1=(),
    start_node_coord2=(),
    end_node_coord1=(18.00538846137929, -76.74990488302866),
    end_node_coord2=(18.005363739833108, -76.7499482540394),
    use_connected_path_end_for_start=True,
    connected_path=11,
    map_area_id=1)

addPath(
    name="Spine SLT 3",
    start_node_coord1=(),
    start_node_coord2=(),
    end_node_coord1=(18.00551361211023, -76.74997399117024),
    end_node_coord2=(18.00549045850343, -76.75002768069749),
    use_connected_path_end_for_start=True,
    connected_path=12,
    map_area_id=1)

# intersection joining the entrance behind library with spine
addPath(
    name="Back of SLT 2",
    start_node_coord1=(18.00519609498825, -76.74983369568717),
    start_node_coord2=(18.00523492911374, -76.74986128848244),
    end_node_coord1=(18.00551441427108, -76.74943755702088),
    end_node_coord2=(18.00553981822108, -76.74948037982531),
    use_connected_path_end_for_start=False,
    connected_path=11,
    map_area_id=1)

addPath(
    name="Back of Sci-Tech Library",
    start_node_coord1=(),
    start_node_coord2=(),
    end_node_coord1=(18.00563074077843, -76.74940123712422),
    end_node_coord2=(18.00564192039173, -76.74944775230682),
    use_connected_path_end_for_start=True,
    connected_path=14,
    map_area_id=1)

"""
add the starting points
"""
addStartingPoint(
    name="Juici Patty Entrance",
    map_area_id=1,
    coord=(18.005641200051024, -76.74857047250477),
    connected_path=1)

addStartingPoint(
    name="Chemistry Department Entrance",
    map_area_id=1,
    coord=(18.004440018221864, -76.74949937845855),
    connected_path=9)

addStartingPoint(
    name="Entrance Behind Faculty Library",
    map_area_id=1,
    coord=(18.005641096894426, -76.74942306764507),
    connected_path=15)

"""
add buildings
"""
addBuilding(
    name="Science and Technology Library",
    address1="2742+46",
    address2="Kingston, Jamaica",
    address3="",
    image_url="sci_tech_library.jpg",
    b_type="Library",
    info="The main Library of the Sci- Tech faculty",
    coord=(18.005339, -76.749472),
    connected_path=3,
    stop_node_coord1=(18.005253825739608, -76.74939966007331),
    stop_node_coord2=(18.005212253807578, -76.74936965974061))

addBuilding(
    name="Science Lecture Theatre 2",
    address1="2742+34",
    address2="Kingston, Jamaica",
    address3="",
    image_url="slt_2.jpg",
    b_type="Lecture Theatre",
    info="SLT 2",
    coord=(18.005164, -76.749748),
    connected_path=10,
    stop_node_coord1=(18.00508708982741, -76.74978257354715),
    stop_node_coord2=(18.00507595121626, -76.74980007427195))

addBuilding(
    name="Science Lecture Theatre 1",
    address1="2742+32",
    address2="Kingston, Jamaica",
    address3="",
    image_url="slt_1.jpg",
    b_type="Lecture Theatre",
    info="SLT 1",
    coord=(18.005172, -76.749948),
    connected_path=11,
    stop_node_coord1=(18.005175987816227, -76.74982345423909),
    stop_node_coord2=(18.00516487330864, -76.74984974964948))

addBuilding(
    name="Science and Technology Faculty Office",
    address1="2742+32",
    address2="Kingston, Jamaica",
    address3="",
    b_type="Office",
    info="The faculty and Deans office",
    coord=(18.005356, -76.749883),
    connected_path=12,
    stop_node_coord1=(18.00537054360944, -76.74992275972095),
    stop_node_coord2=(18.005359413032878, -76.7499563325051))

addBuilding(
    name="Aunty Jackie\'s Shop",
    address1="2742+24",
    address2="Kingston, Jamaica",
    address3="",
    image_url="aunty_jackie_stall.jpg",
    b_type="Stall",
    info="Aunty Jackie\'s Food and Supplies Shop",
    coord=(18.005061, -76.749630),
    connected_path=4,
    stop_node_coord1=(18.005073691484913, -76.74965550265733),
    stop_node_coord2=(18.005034899271298, -76.74963960260932))

addBuilding(
    name="Mathematics Department",
    address1="2732+X5",
    address2="Kingston, Jamaica",
    address3="",
    b_type="Department",
    info="The main mathematics department",
    coord=(18.004896403305285, -76.74950881202325),
    connected_path=6,
    stop_node_coord1=(18.004832295731436, -76.7496739184623),
    stop_node_coord2=(18.004885183785383, -76.74961612657061))

addBuilding(
    name="Science Lecture Theathre 3",
    address1="264X+6W",
    address2="Kingston, Jamaica",
    address3="",
    b_type="Lecture Theathre",
    info="The third science lecture theathre",
    coord=(18.005509748043483, -76.75014063633235),
    connected_path=13,
    stop_node_coord1=(18.005492828634214, -76.74996558704959),
    stop_node_coord2=(18.005467896892632, -76.75002393082016))

"""
add OD objects
"""
add_OD_Objects(
    name="Aunty Jackie Stall",
    object_name="18.0050609_-76.7496662_auntyjackie",
    map_zone=4,
    building_id=None,
    coord=(18.0050609, -76.7496662))

add_OD_Objects(
    name="Aunty Jackie Bench",
    object_name="18.0050864_-76.7496363_bench",
    map_zone=4,
    building_id=None,
    coord=(18.0050864, -76.7496363))

add_OD_Objects(
    name="Sci-Tech Library Stall",
    object_name="18.0051667_-76.74944412_librarystall",
    map_zone=3,
    building_id=None,
    coord=(18.0051667, -76.74944412))

add_OD_Objects(
    name="Science Lecture Theatre 1 Door",
    object_name="18.0051836_-76.7497262_pclt1",
    map_zone=None,
    building_id=3,
    coord=(18.0051836, -76.7497262))

add_OD_Objects(
    name="Sci-Tech entrance recycle bin",
    object_name="18.0053245_-76.7486424_recyclebin",
    map_zone=1,
    building_id=None,
    coord=(18.0053245, -76.7486424))

add_OD_Objects(
    name="Sci-Tech entrance Sign",
    object_name="18.0055634_-76.7484079_scitechsign",
    map_zone=1,
    building_id=None,
    coord=(18.0055634, -76.7484079))

add_OD_Objects(
    name="Sci-Tech Library Sign",
    object_name="18.0053644_-76.7493880_librarysign",
    map_zone=3,
    building_id=None,
    coord=(18.0053644, -76.7493880))

add_OD_Objects(
    name="Sci-Tech Physics Department Sign",
    object_name="18.0053657_-76.7491452_physicssign",
    map_zone=2,
    building_id=None,
    coord=(18.0053657, -76.7491452))

add_OD_Objects(
    name="Sci-Tech blue sign",
    object_name="18.0053530_-76.7490375_signatentrancetoscitech",
    map_zone=2,
    building_id=None,
    coord=(18.0053530, -76.7490375))

"""
add demo events
"""
addEvent(
    building_id=1,
    name="COMP3901 Presentation",
    start_time=datetime.time(0,0,0),
    end_time=datetime.time(23,59,59),
    recurrent=True,
    day_of_week=2,
    specific_date=None,
    info="An event for the capstone demo")

addEvent(
    building_id=2,
    name="COMP3901 Presentation",
    start_time=datetime.time(0,0,0),
    end_time=datetime.time(23,59,59),
    recurrent=True,
    day_of_week=2,
    specific_date=None,
    info="An event for the capstone demo")

addEvent(
    building_id=3,
    name="COMP3901 Presentation",
    start_time=datetime.time(0,0,0),
    end_time=datetime.time(23,59,59),
    recurrent=True,
    day_of_week=2,
    specific_date=None,
    info="An event for the capstone demo")

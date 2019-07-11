from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in meters
class DistanceModel():
    def distance_cal(LatC,LongC,LatT,LongT):
        R = 6373.0

        lat1 = radians(LatC)
        lon1 = radians(LongC)
        lat2 = radians(LatT)
        lon2 = radians(LongT)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

    #    print("Result:", distance)
        return distance
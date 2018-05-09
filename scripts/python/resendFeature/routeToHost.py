import os

class RouteEntablishedDetector:

    def __init__(self, hostIp):
        self.hostIp = hostIp

    def is_entablished_route(self):
        flag = self.__make_ping()
        return flag == True

    def __make_ping(self):
        result = True if os.system("ping -c 1 " + self.hostIp) is 0 else False
        return result

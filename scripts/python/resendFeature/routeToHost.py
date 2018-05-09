import os

class RouteEntablishedDetector:

    def __init__(self, hostIp):
        self.hostIp = hostIp

    def isEntablishedRoute(self):
        flag = self.__makePing()
        return flag == True

    def __makePing(self):
        result = True if os.system("ping -c 1 " + self.hostIp) is 0 else False
        return result

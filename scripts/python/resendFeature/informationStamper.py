import time, datetime

class InformationStamper:

    def __init__(self, list_stampers):
        self.stampers = list_stampers

    def stamp_info(self, json_object):
        for stamper in self.stampers:
            stamper.stamp(json_object)

class TimestampStamper:

    def stamp(self,json_object):
        ts = time.time()
        json_object['timestamp'] = datetime.datetime.fromtimestamp(ts).isoformat()

class IpStamper:

    def __init__(self):
        self.IP_LOCAL_NODE = 'cambiaresto'

    def stamp(self, json_object):
        json_object['ip'] = self.IP_LOCAL_NODE

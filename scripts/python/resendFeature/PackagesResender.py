class PackageResender:

    def __init__(self, line_reader, udpSender):
        self.line_reader = line_reader
        self.udpSender = udpSender

    def resend_all_buffered_packets(self):
        while (not self.line_reader.is_end_of_file()):
            udpPackage = self.line_reader.getLine()
            print(udpPackage)
            udpSender.send(udpPackage)

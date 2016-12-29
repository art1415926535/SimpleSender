import sys
import bluetooth


class SimpleSender:

    def __init__(self):
        self.bd_addr = ""
        self.bd_name = ""

    def connect(self, name=''):
        selected = self.__choose_device(name)
        self.__socket_connect()

    def __choose_device(self, name):
        print("Searching for", name)
        nearby_devices = bluetooth.discover_devices()
        selection = -1
        for i, device in enumerate(nearby_devices):
            if name == bluetooth.lookup_name(device):
                selection = i

        if 0 <= selection < len(nearby_devices):
            self.bd_addr = nearby_devices[selection]
            self.bd_name = bluetooth.lookup_name(nearby_devices[selection])
            return True
        else:
            print("Device not found")
            return False

    def __socket_connect(self):
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        port = 0
        max_port = 3
        connected = False

        print("Connecting...")
        while not connected and port <= max_port:
            try:
                self.sock.connect((self.bd_addr, port))
                connected = True
                print("Connected!")
            except:
                port += 1
        if port > max_port:
            print("Connected error: port detection failed")
            self.disconnect()

    def disconnect(self):
        self.sock.close()
        self.bd_addr = ''
        self.bd_name = ''
        print("Disconnected!")

    def send(self, data=''):
        if self.bd_addr:
            self.sock.send(bytes(data, 'UTF-8'))
            print("Send '{}'".format(data))
        else:
            print("Error: socket not bound.")


if __name__ == '__main__':
    sender = SimpleSender()
    sender.connect(sys.argv[1])
    sender.send(sys.argv[2])
    sender.disconnect()

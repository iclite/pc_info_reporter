from datetime import datetime
import socket
import json
import threading

hosts = socket.gethostbyname_ex(socket.gethostname())[2]
port = 57000

def get_host_ip():
    return socket.gethostbyname_ex(socket.gethostname())[2]

def timestamp():
    return datetime.fromtimestamp(datetime.timestamp(datetime.now()))

class DiscoverThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(DiscoverThread, self).__init__(*args, **kwargs)
        self._stopper = threading.Event()
        self.ds = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ds.settimeout(1)
        self.ds.bind(('', port))

    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.is_set()

    def run(self):
        while True:
            if self.stopped():
                self.ds.close()
                return
            ds_data = None
            ds_address = None

            try:
                ds_data, ds_address = self.ds.recvfrom(1024)
            except socket.timeout:
                pass

            if ds_data and ds_data.decode('utf-8') == '-*-*-Computer-Information*Report-*-*-':
                self.ds.sendto("*-*-*Computer*Information-Report*-*-*".encode('utf-8'), ds_address)
                print(f'[{timestamp()}] Discover server found [{ds_address[0]}].')

class ReportThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(ReportThread, self).__init__(*args, **kwargs)
        self._stopper = threading.Event()
        self.rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rs.bind(("", port))
        self.rs.settimeout(1)
        self.rs.listen(30)

    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.is_set()

    def run(self):
        for host in hosts:
            print(f'[{timestamp()}] Server running, IP is [{host}]')

        while True:
            if self.stopped():
                self.rs.close()
                return

            connection = None
            address = None

            try:
                connection, address = self.rs.accept()
            except socket.timeout:
                pass

            if connection and address:
                address = address[0]
                print(f'[{timestamp()}] {address} connected.')

                while True:
                    data = connection.recv(1024)
                    if not data:
                        break

                    pc = json.loads(data.decode("utf-8"))

                    print(f'[{timestamp()}] {address} [{pc["brand"]} - {pc["model"]} - {pc["serial"]}] computer information has been reported!')
                    print(f'[{timestamp()}] {address} [{pc}]')
                    back = data.decode('utf-8')
                    connection.sendall(back.encode('utf-8'))

                print(f'[{timestamp()}] {address} disconnected.')
                connection.close()

if __name__ == '__main__':
    discover_server = DiscoverThread()
    report_server = ReportThread()

    discover_server.start()
    report_server.start()



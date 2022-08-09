from datetime import datetime
import socket
import json
import threading

hosts = socket.gethostbyname_ex(socket.gethostname())[2]
port = 57000

def timestamp():
    return datetime.fromtimestamp(datetime.timestamp(datetime.now()))

def discover_thread():
    ds = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ds.settimeout(1)
    ds.bind(('', port))

    while True:
        ds_data = None
        ds_address = None
        
        try:
            ds_data, ds_address = ds.recvfrom(1024)
        except socket.timeout:
            pass

        if ds_data and ds_data.decode('utf-8') == '-*-*-Computer-Information*Report-*-*-':
            ds.sendto("*-*-*Computer*Information-Report*-*-*".encode('utf-8'), ds_address)
            print(f'[{timestamp()}] Discover server found [{ds_address[0]}].')

def report_thread():
    report_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    report_socket.bind(("", port))
    report_socket.listen(30)

    while True:
        connection, address = report_socket.accept()
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
    discover_server = threading.Thread(target=discover_thread)
    report_server = threading.Thread(target=report_thread)

    discover_server.start()
    report_server.start()

    for host in hosts:
        print(f'[{timestamp()}] Server running, IP is [{host}]')

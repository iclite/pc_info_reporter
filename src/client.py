from datetime import datetime
import socket
import json

import wmi

def get_computer_info():
    c = wmi.WMI()

    computer = c.Win32_ComputerSystem()[0]
    brand = computer.Manufacturer
    model = computer.SystemFamily
    serial = computer.Model

    processor = c.Win32_Processor()[0]
    cpu_name = processor.Name

    memory = c.Win32_PhysicalMemory()[0]
    ram_size = str(int(int(memory.Capacity)/1024/1024/1024)) + 'G'

    disks = c.Win32_DiskDrive()[0]
    disk_size = str(int(int(disks.Size)/1000/1000/1000)) + 'G'

    os = c.Win32_OperatingSystem()[0]
    os_name = os.Caption
    os_architecture = os.OSArchitecture

    return {
        'brand': brand,
        'model': model,
        'serial': serial,
        'cpu': cpu_name,
        'ram': ram_size,
        "rom": disk_size,
        "os": os_name,
        "architecture": os_architecture
    }

def timestamp():
    return datetime.fromtimestamp(datetime.timestamp(datetime.now()))

def discover_client():
    discover_address = ('<broadcast>', 57000)
    discover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discover_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    data = "-*-*-Computer-Information*Report-*-*-".encode('utf-8')
    discover_socket.sendto(data, discover_address)

    print(f'[{timestamp()}] Server discovering')

    while True:
        discover_data, discover_address = discover_socket.recvfrom(1024)
        if discover_data.decode('utf-8') == "*-*-*Computer*Information-Report*-*-*":
            print(f'[{timestamp()}] Server discovered: {discover_address[0]}')
            return (discover_address[0], 57000)

def report_client(server_address):
    message = get_computer_info()
    message = json.dumps(message, ensure_ascii=False).encode('utf-8')
    sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_obj.connect(server_address)
    sock_obj.sendall(message)
    data = sock_obj.recv(1024)
    if data == message:
        print(f'[{timestamp()}] Computer Report Success!')
    else:
        print(f'[{timestamp()}] Computer Report Error! Data not match.')

    sock_obj.close()

if __name__ == '__main__':
    server_address = discover_client()

    report_client(server_address)

from datetime import datetime
import socket
import json

import wmi

def get_computer_info():
    c = wmi.WMI()

    computer = c.Win32_ComputerSystem()[0]
    brand = computer.Manufacturer
    model = computer.Model

    bios = c.Win32_BIOS()[0]
    serial = bios.SerialNumber

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
    discover_socket.settimeout(1)
    data = "-*-*-Computer-Information*Report-*-*-".encode('utf-8')

    while True:
        try:
            print(f'[{timestamp()}] Server discovering')
            discover_socket.sendto(data, discover_address)
            discover_data, discover_address = discover_socket.recvfrom(1024)

            if discover_data.decode('utf-8') == "*-*-*Computer*Information-Report*-*-*":
                print(f'[{timestamp()}] Server discovered: {discover_address[0]}')
                return (discover_address[0], 57000)
        except socket.timeout:
            pass

def report_client(server_address):
    message = get_computer_info()
    message = json.dumps(message, ensure_ascii=False).encode('utf-8')
    sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_obj.connect(server_address)
    sock_obj.sendall(message)
    data = sock_obj.recv(1024)
    sock_obj.close()
    if data == message:
        print(f'[{timestamp()}] Computer Report Success!')
        return True
    else:
        print(f'[{timestamp()}] Computer Report Error! Data not match.')
        return False

def report_info():
    server_address = discover_client()

    return report_client(server_address)

if __name__ == '__main__':
    report_info()

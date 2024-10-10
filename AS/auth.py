import socket
import json

filename = 'records.json'


def register(data):
    reg = data.split('\n')
    record = {}
    for line in reg:
        if '=' in line:
            k, v = line.split('=')
            record[k] = v
    if 'NAME' in record and 'VALUE' in record:
        try:
            with open(filename, 'r') as f:
                dns_records = json.load(f)
        except FileNotFoundError:
            dns_records = {}
        dns_records[record['NAME']] = record['VALUE']
        with open(filename, 'w') as f:
            json.dump(dns_records, f)
        return 'Done'
    return 'Invalid Registration'


def query_response(data):
    que = data.split('\n')
    query = {}
    for line in que:
        if '=' in line:
            k, v = line.split('=')
            query[k] = v
    if 'NAME' in query:
        try:
            with open(filename, 'r') as f:
                dns_records = json.load(f)
            if query['NAME'] in dns_records:
                return f"TYPE=A\nNAME={query['NAME']}\nVALUE={dns_records[query['NAME']]}\nTTL=10\n"
            else:
                return 'DNS Not Found'
        except FileNotFoundError:
            return 'No DNS File Yet'
    return 'Invalid Query'


if __name__ == '__main__':
    server_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_soc.bind(('0.0.0.0', 53533))
    while True:
        data, address = server_soc.recvfrom(1024)
        message = data.decode()
        if 'VALUE' in message:
            response = register(message)
        else:
            response = query_response(message)
        server_soc.sendto(response.encode(), address)

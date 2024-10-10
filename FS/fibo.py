from flask import Flask, request, jsonify
import requests
import socket
import json

app = Flask(__name__)


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def register_as(hostname, ip, as_ip, as_port, ttl):
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    r_str = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r_str.sendto(message.encode(), (as_ip, int(as_port)))
    data, _ = r_str.recvfrom(1024)
    r_str.close()
    return data.decode()


@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    hostname = data['hostname']
    ip = data['ip']
    as_ip = data['as_ip']
    as_port = data['as_port']
    if not all([hostname, ip, as_ip, as_port]):
        return "bad request", 400
    # maybe randint?
    ttl = 10
    response = register_as(hostname, ip, as_ip, as_port, ttl)
    return jsonify({"message": "Registered", "as_response": response}), 201


@app.route('/fibonacci')
def get_fibonacci():
    number = request.args.get('number')
    try:
        num_int = int(number)
    except ValueError:
        return jsonify({'error': 'Type Error'}), 400
    if num_int < 0:
        return jsonify({'error': 'Invalid Number'}), 400
    res = fibonacci(num_int)
    return jsonify({'fibonacci': res}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=9090,
            debug=True)
import requests
from flask import Flask, request, jsonify
import socket

app = Flask(__name__)


def query(hostname, as_ip, as_port):
    message = f"TYPE=A\nNAME={hostname}\n"
    q_str = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    q_str.sendto(message.encode(), (as_ip, int(as_port)))
    data, _ = q_str.recvfrom(1024)
    q_str.close()
    response = data.decode().split('\n')
    fs_ip = next(line.split('=')[1] for line in response if line.startswith('VALUE='))
    return fs_ip


@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    hostname, fs_port, number, as_ip, as_port = request.args.get('hostname'), \
                                                request.args.get('fs_port'), \
                                                request.args.get('number'), \
                                                request.args.get('as_ip'), \
                                                request.args.get('as_port')
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "bad request", 400
    try:
        fs_ip = query(hostname, as_ip, as_port)
        fib = requests.get(f"http://{fs_ip}:{fs_port}/fibonacci", params={"number": number})
        return jsonify({"fibonacci": fib.json()["fibonacci"]}), 200
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)

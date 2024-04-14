import argparse
import json
from obswebsocket import obsws, requests

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='IP address of the OBS server')
    parser.add_argument('--port', help='Port of the OBS server')
    parser.add_argument('--password', help='Password for the OBS server')
    parser.add_argument('--conn_conf_path', help='Path to the file containing the connection configuration for the OBS server')
    parser.add_argument('--command', help='Command to send to the OBS server')
    parser.add_argument('--script', help='Command to send to the OBS server')
    args = parser.parse_args()

    ip_conf_cnt = 1 if args.ip is not None else 0 + \
                  1 if args.conn_conf_path is not None else 0
    if ip_conf_cnt != 1:
        print('Must specify either ip or conn_conf_path')
        exit(1)
    
    port_conf_cnt = 1 if args.port is not None else 0 + \
                    1 if args.conn_conf_path is not None else 0
    if port_conf_cnt != 1:
        print('Must specify either port or conn_conf_path')
        exit(1)

    password_conf_cnt = 1 if args.password is not None else 0 + \
                        1 if args.conn_conf_path is not None else 0
    if password_conf_cnt != 1:
        print('Must specify either password or conn_conf_path')
        exit(1)

    command_conf_cnt = 1 if args.command is not None else 0 + \
                       1 if args.script is not None else 0
    if command_conf_cnt != 1:
        print('Must specify either command or script')
        exit(1)

    if args.ip is not None:
        ip = args.ip
    if args.port is not None:
        port = args.port
    if args.password is not None:
        password = args.password
    if args.conn_conf_path is not None:
        with open(args.conn_conf_path, 'r') as file:
            ip, port, password = file.readlines()
            ip = ip.strip()
            port = int(port.strip())
            password = password.strip()
    if args.command is not None:
        command_list = [args.command]
    if args.script is not None:
        with open(args.script, 'r') as file:
            command_list = file.readlines()
    
    ws = obsws(ip, port, password)
    ws.connect()
    for command in command_list:
        json_data = json.loads(command)
        requestType = json_data['requestType']
        requestFields = json_data.get('requestFields', {})
        responseField = json_data.get('responseField', None)
        request_call = getattr(requests, requestType)
        response = ws.call(request_call(**requestFields))
        if responseField is not None:
            print(response.datain[responseField])
    ws.disconnect()

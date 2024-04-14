import argparse
from obswebsocket import obsws, requests

COMMANDTYPE_TO_FUNC = {}
def command_to_action(command):
    command = command.strip()
    command = command.lower()
    command = command.split(' ')
    action_type = command[0]
    if action_type in COMMANDTYPE_TO_FUNC:
        return COMMANDTYPE_TO_FUNC[action_type](command)
    else:
        print('Invalid command: ' + action_type)
        exit(1)

def cmd_version(command):
    def _ret(ws):
        print(ws.call(requests.GetVersion()).getObsVersion())
    return _ret
COMMANDTYPE_TO_FUNC['version'] = cmd_version

def cmd_set_source_filter_enabled(command):
    def _ret(ws):
        source_name = command[1]
        filter_name = command[2]
        filter_enabled = strtobool(command[3])
        ws.call(requests.SetSourceFilterEnabled(sourceName=source_name, filterName=filter_name, filterEnabled=filter_enabled))
    return _ret
COMMANDTYPE_TO_FUNC['set_source_filter_enabled'] = cmd_set_source_filter_enabled

def get_password(password_path):
    with open(password_path, 'r') as file:
        return file.read().strip()

def strtobool(val):
    if val is None: return False
    return val.lower() not in ('n', 'no', 'f', 'false', 'off', '0', '')
    
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

    action_list = map(command_to_action, command_list)

    ws = obsws(ip, port, password)
    ws.connect()
    for action in action_list:
        action(ws)
    ws.disconnect()

import re
import socket
import socketserver
import yaml


class SyslogRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()  # Get the data sent to the server
        log = data.decode()
        print(f'Received log: {log}')

        # Match the log against the patterns
        for pattern, port in patterns:
            if pattern.match(log):
                print(f'Matching log: {log} will be forwarded to port {port}')
                self.forward_log(log, port)
                break  # Forward to only one port per log entry

    def forward_log(self, log, port):
        # Create a syslog UDP socket for forwarding
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as forward_sock:
            forward_sock.sendto(log.encode(), ('localhost', port))
            print(f'Forwarded log to port {port}')


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def main():
    global patterns
    # Load configuration
    config = load_config('config.yaml')

    # Prepare regex patterns and ports
    patterns = []
    for item in config['input']:
        patterns.append((re.compile(item['regex']), item['port']))

    # Create a UDP server to listen for incoming syslog messages
    server = socketserver.UDPServer(('0.0.0.0', 514), SyslogRequestHandler)
    print('Listening for incoming syslog messages on port 514...')
    
    try:
        server.serve_forever()  # Start the server
    except KeyboardInterrupt:
        print("Stopping the syslog listener.")
        server.server_close()


if __name__ == '__main__':
    main()



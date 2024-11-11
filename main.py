import socket
import socketserver
from utils import load_config, process_config


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
            forward_sock.sendto(log.encode(), ('127.0.0.1', port))
            print(f'Forwarded log to port {port}')


def main():
    global patterns
    # Load configuration
    config = load_config('/etc/syslog-flow/config.yaml')
    patterns = process_config(config)

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

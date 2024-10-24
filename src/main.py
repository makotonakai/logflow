import re
import socket
import yaml
import syslog
import time


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def forward_log(log, port):
    # Create a syslog UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(log.encode(), ('localhost', port))
    sock.close()


def main():
    # Load configuration
    config = load_config('config.yaml')

    # Prepare regex patterns and ports
    patterns = []
    for item in config['input']:
        patterns.append((re.compile(item['regex']), item['port']))

    # Simulated log input (you would replace this with actual log input)
    simulated_logs = [
        '127.0.0.1:53483 [24/Oct/2024:22:55:47.110] http-in servers/server2 0/0/0/1/1 200 315 - - ---- 2/2/0/0/0 0/0 {localhost} "GET / HTTP/1.1"',
        '127.0.0.1:53597 [24/Oct/2024:22:57:23.552] stats stats/<STATS> 0/0/0/-1/0 400 469 - - LR-- 2/1/0/0/0 0/0 "GET /stats HTTP/1.1"',
        # Add more logs as needed for testing
    ]

    # Process each log entry
    for log in simulated_logs:
        for pattern, port in patterns:
            if pattern.match(log):
                print(f'Matching log: {log} will be forwarded to port {port}')
                forward_log(log, port)
                break  # Forward to only one port per log entry
            # else:
            #     print("log forwarding failed")
            #     break


if __name__ == '__main__':
    main()

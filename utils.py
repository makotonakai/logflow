import re
import yaml
from errors import ConfigError

HAPROXY_ACCESS_LOG_REGEX = r'^<[0-9]+>[A-Za-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ [a-z]+\[[0-9]+\]: ((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}:[0-9]+ \[[0-9]+\/[A-Za-z]+\/[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}\] [a-z-]+ [a-z]+\/[0-9A-Za-z]+ [0-9-]+\/[0-9-]+\/[0-9-]+\/[0-9-]+\/[0-9-]+ [0-9]+ [0-9]+ [0-9A-Za-z-] [0-9A-Za-z-] [0-9A-Za-z-]+ [0-9-]+\/[0-9-]+\/[0-9-]+\/[0-9-]+\/[0-9-]+ [0-9-]+\/[0-9-]+ \{[A-Za-z0-9]+\} \"[A-Z]+ [a-z/]+ [A-Z]+\/[0-9.]+\"$'
HAPROXY_STATS_LOG_REGEX = r'^<[0-9]+>[A-Za-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ [a-z]+\[[0-9]+\]: ((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}:[0-9]+ \[[0-9]+\/[A-Za-z]+\/[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}\] [a-z-]+ [a-z]+\/\<[0-9A-Za-z]+\> [0-9-]+\/[0-9-]+\/[0-9-]+\/[0-9-]+\/[0-9-]+ [0-9]+ [0-9]+ [0-9A-Za-z-]+ [0-9A-Za-z-]+ [0-9A-Za-z-]+ [0-9-]+\/[0-9-]+\/[0-9-]+\/[0-9-]+\/[0-9-]+ [0-9-]+\/[0-9-]+ \"[A-Z]+ [a-z/]+ [A-Z]+\/[0-9.]+\"$'
HAPROXY_ERROR_LOG_REGEX = r'^<[0-9]+>[A-Za-z]+ [0-9]+ [0-9]+:[0-9]+:[0-9]+ [a-z]+\[[0-9]+\]: [A-Za-z0-9():\-\_\,\. ]+$'


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def process_config(config):

    if 'config' not in config:
        raise ConfigError("Config key doesn't exist in the config file")

    if 'haproxy' not in config['config']:
        raise ConfigError("haproxy key doesn't exist in the config file")

    patterns = []
    for item in config['config']['haproxy']:
        if item['kind'] == 'access_log':
            regex = HAPROXY_ACCESS_LOG_REGEX
        elif item['kind'] == 'stats_log':
            regex = HAPROXY_STATS_LOG_REGEX
        elif item['kind'] == 'error_log':
            regex = HAPROXY_ERROR_LOG_REGEX
        else:
            raise ConfigError("You can specify only specify access_log, stats_log, or error_log")

        if 'port' not in item:
            raise ConfigError("Port is not specified")

        port = item['port']

        patterns.append((re.compile(regex), port))

    return patterns

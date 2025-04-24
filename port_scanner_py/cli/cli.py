from .port_parser import parse_ports
from .host_parser import parse_hosts
import argparse

TOP_1000_PORTS_FILE = "./data/ports.txt"

def get_args():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--host", nargs="+", help="List of IP or ranges", type=str, required=True)

    port_group = parser.add_mutually_exclusive_group(required=False)
    port_group.add_argument("-p", "--port", nargs="+", help="List of ports or ranges", type=str)
    port_group.add_argument("--ports-file", help="Path to a file containing list of ports", type=str)

    args = parser.parse_args()
    args.host = parse_hosts(args.host)
    if args.port:
        args.port = parse_ports(ports=args.port)
    else:
        ports_file = args.ports_file or TOP_1000_PORTS_FILE
        args.port = parse_ports(ports_file=ports_file)

    return args

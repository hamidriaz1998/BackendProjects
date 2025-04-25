from cli.cli import get_args
from port_scanner.scanner import scan_ports

args = get_args()
hosts, ports = args.host, args.port

scan_ports(hosts, ports)

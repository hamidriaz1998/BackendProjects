from cli.cli import get_args
from port_scanner.scanner import scan_ports

args = get_args()
hosts, ports, timeout = args.host, args.port, args.timeout

scan_ports(hosts, ports, timeout)

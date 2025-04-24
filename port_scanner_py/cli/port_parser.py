import argparse

def parse_port(value:str) -> list[int]:
    if "-" in value:
        parts = value.split("-")
        if len(parts) != 2:
            raise argparse.ArgumentTypeError(f"Invalid Port range: {value}")

        try:
            start,end = list(map(int, parts))
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid Port format: {value}")
        if end < start:
            raise argparse.ArgumentTypeError(f"Invalid Port range: {value}")
        return list(range(start, end+1))
    else:
        return [int(value)]

def parse_ports(ports:list[str]=[], ports_file:str=""):
    if ports:
        result = []
        for p in ports:
            result.extend(parse_port(p))
        return result

    if ports_file:
        try:
            with open(ports_file, 'r') as f:
                result = []
                for line in f:
                    line = line.strip()
                    ports = line.split(",")
                    for p in ports:
                        result.extend(parse_port(p))
                return result
        except FileNotFoundError:
            raise FileNotFoundError(f"Ports file not found: {ports_file}")
    
    raise ValueError("Either port or ports_file must be provided")
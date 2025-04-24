from cli.cli import get_args

args = get_args()

for p in args.port:
    print(p)
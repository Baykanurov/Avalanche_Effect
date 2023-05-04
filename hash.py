from src import parser, Manager

args = parser.parse_args()

if __name__ == "__main__":
    manager = Manager(file=args.file, text=args.text, output=args.output)
    result = ""
    if args.text:
        result = manager.get_hash(data=args.text.encode())
    elif args.file:
        try:
            data = manager.read_file()
        except FileNotFoundError as error:
            print(error)
            exit(1)
        result = manager.get_hash(data=data)
    else:
        parser.print_help()
        exit(1)

    if args.output:
        manager.write_file(result=result)

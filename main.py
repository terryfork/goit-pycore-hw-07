import commands


def main():
    print("Hello friend! This is CLI bot. Please enter command.")
    while not commands.done:
        console_line = ""
        while console_line == "":
            console_line = input(">")
        command, params = parse_input(console_line)
        handler_name = command+"_handler"
        if handler_name in dir(commands):
            handler = getattr(commands, handler_name)
            print(handler(params))
        else:
            print(
                "Command not recognized. "
                "Type 'help' to print available commands"
            )


def parse_input(line):
    words = line.split(" ")
    command = words.pop(0).lower().replace("-","_")
    return command, words


if __name__ == "__main__":
    main()

import sys

##### TEXT AND CONSTS #####

## Every times anyone cracks it (you reading this code or someone else)
## I'll try making a new MayChen-Crypt version in response to the attention :3
VERSION = b'1'

MAGIC_NUMBER = b'\x4D\x41\x59\x43\x48\x45\x4E\x43\x52\x59\x50\x54' + VERSION

HELP_MSG = "MayChen-Crypt v" + str(VERSION, "utf-8") + "\nUsage: MayChen-Crypt.py [(encode/decode)] [FILEPATH] [KEY]"

##### UTILS #####
END = 0

program_end = lambda: print("Program terminated.")
sequence = lambda f_result: program_end() if f_result == END else lambda f_next: sequence(f_next)

isThisText = lambda x: lambda smth: x.lower() == smth
ifTrueThenDoOrElse = lambda cond: lambda do: do() if cond else lambda elze: elze() ## Fix this

##### COMMON #####

##### ENCODER #####
encode = lambda file_path: lambda key: print("Placeholder")

##### DECODER #####
decode = lambda file_path: lambda key: print("Placeholder")

##### ENTRY POINT #####
isEncodeOrElse = lambda args: ifTrueThenDoOrElse (isThisText(args[1])("encode")) (lambda: encode(args[1])(args[2])) ## Those two
isDecodeOrElse = lambda args: ifTrueThenDoOrElse (isThisText(args[1])("decode")) (lambda: decode(args[1])(args[2])) ## Might be weird

main = lambda args: isEncodeOrElse (args) (lambda: isDecodeOrElse (args) (lambda: print(HELP_MSG)) ) ## This doesn't work

if __name__ == "__main__":
    main(sys.argv)

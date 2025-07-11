import sys

## Every times someone crack it (you reading this code or someone else)
## I'll try making a new MayChen-Crypt version :3
version = b'1'

##### Utils #####
END = 0

program_end = lambda: print("Program terminated.")
sequence = lambda f_result: program_end() if f_result == END else lambda f_next: sequence(f_next)

##### Entry point #####
main = lambda args: sequence(print("1")) (print(args[1])) (print("ww")) (END)

##### ENCODER #####
magic_number = b'\x4D\x41\x59\x43\x48\x45\x4E\x43\x52\x59\x50\x54' + version

if __name__ == "__main__":
    main(sys.argv)

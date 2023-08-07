import sys

filename = ""
if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print(f"Usage: {sys.argv[0]} filename")
    sys.exit(1)

file = open(filename, "rb")
source = file.read()
file.close()

index = 0
while index < len(source):
    print(f"{index:04x} ", end="")
    b = 0
    while b < 8 and index + b < len(source):
        print(f"{source[index + b]:02x} ", end="")
        b += 1
    print()
    index += 8
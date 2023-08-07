from Const import *
import json
import sys

def between(num, start, end):
    return num >= start and num <= end

def is_word(adr):
    for entry in word_table:
        if between(adr, int(entry["start"], 16), int(entry["end"], 16)):
            return True
    return False

def is_byte(adr):
    for entry in byte_table:
        if between(adr, int(entry["start"], 16), int(entry["end"], 16)):
            return True
    return False

dis_opcodes = [None for x in range(256)]

for op in OPCODES.keys():
    keys = OPCODES[op].keys()
    for key in keys:
        dis_opcodes[OPCODES[op][key]] = { "monic": op, "addressing_mode": key }

# source = [0x00,0xc0, 0x78, 0xa9, 0x12, 0x8d, 0x14, 0x03, 0xa9, 0xc0, 0x8d, 0x15, 0x03, 0xa9, 0x93, 0x20, 0xd2, 0xff, 0x58, 0x60, 0x4c, 0x31, 0xea]

filename_json = None
# filename_bin = "a.out"

if len(sys.argv) > 1:
    if sys.argv[1].endswith(".json"):
        filename_json = sys.argv[1]
    else:
        filename_bin = sys.argv[1]
else:
    print(f"Usage: [sys.argv[0]] infile | infile.json")
    sys.exit(1)

byte_table = []
word_table = []

data = None
index = 0

if filename_json:
    json_file = open(filename_json)
    json_data = json_file.read()
    json_file.close()

    data = json.loads(json_data)

    filename_bin = data["filename"]
    byte_table = data["byte_table"]
    word_table = data["word_table"]

source_file = open(filename_bin, "rb")
source = source_file.read()
source_file.close()

# assume start address is included (C= like)
start_adr = source[0] + 256 * source[1]
source = source[2:]

labels = set()
disasmd_lines = []

while index < len(source) and index < 10000:
    address = start_adr + index
    b = source[index]

    if is_byte(address):
        if b >= 32 and b <= 122:
            disasmd_lines.append(f'L{address:04x} .by ${b:02x}   ; "{chr(b)}"')
            # print(f'L{address:04x} .by ${b:02x}   ; "{chr(b)}"')
        elif b in (8, 10, 13):
            c = [0,1,2,3,4,5,6,7, "Backspace",9,"Line feed (\\r)",0xb,0xc,"Carriage return (\\n)"][b]
            disasmd_lines.append(f'L{address:04x} .by ${b:02x}   ; "{c}"')

        #
        elif b >= 65 + 128 and b <= 90 + 128 or b == 35 + 128: # "a"-"z", "#"
            disasmd_lines.append(f'L{address:04x} .by ${b:02x}   ; "{chr(b)}" / "{chr(b - 128)}"')
        else:
            disasmd_lines.append(f'L{address:04x} .by ${b:02x}')
        index += 1
        continue

    if is_word(address):
        disasmd_lines.append(f'L{address:04x} .wo ${source[index + 1]:02x}{b:02x}')
        index += 2
        continue

    if dis_opcodes[b] == None:
        disasmd_lines.append(f"L{address:04x} ???")
        index += 1
        continue

    adr_mode = dis_opcodes[b]["addressing_mode"]
    monic = dis_opcodes[b]["monic"]

    # record labels
    if adr_mode >= ZP and adr_mode < IMMEDIATE:
        dest_address = f"L{source[index + 1]:02x}"
        labels.add(dest_address)
    if adr_mode >= ABSOLUTE:
        dest_address = f"L{source[index + 1] + 256 * source[index + 2]:04x}"
        labels.add(dest_address)
    if adr_mode == RELATIVE:
        distance = source[index + 1]
        b_adress = address + distance + 2
        if distance > 127:
            b_adress = address + distance - 254
        dest_address = f"L{b_adress:04x}"
        labels.add(dest_address)

    if adr_mode == IMPLIED:
        disasmd_lines.append(f"L{address:04x} {monic}")
    elif adr_mode in (ZP,RELATIVE, ABSOLUTE):
        disasmd_lines.append(f"L{address:04x} {monic} {dest_address}")
    elif adr_mode in (ZPX, ABSOLUTEX):
        disasmd_lines.append(f"L{address:04x} {monic} {dest_address},x")
    elif adr_mode in (ZPY, ABSOLUTEY):
        disasmd_lines.append(f"L{address:04x} {monic} {dest_address},y")
    elif adr_mode == USELESS:
        disasmd_lines.append(f"L{address:04x} {monic} ({dest_address},x)")
    elif adr_mode == INDIRECTY:
        disasmd_lines.append(f"L{address:04x} {monic} ({dest_address}),y")
    elif adr_mode == IMMEDIATE:
        disasmd_lines.append(f"L{address:04x} {monic} #${source[index + 1]:02x}    ;{source[index + 1]}")
    elif adr_mode == INDIRECT:
        disasmd_lines.append(f"L{address:04x} {monic} ({dest_address})")
    index += 1
    if adr_mode >= RELATIVE:
        index += 1
    if adr_mode >= ABSOLUTE:
        index += 1

# print(labels)
end_adr = start_adr+len(source)-1

for line in disasmd_lines:
    dl_label = line.split(" ")[0]
    dl_rest = line.split(" ", 1)[1]

    # if dl_label in labels:
    #     print(line)
    # else:
    #     print(f"      {dl_rest}")

outfile = open(filename_bin + "_out.txt", "wt")
for label in labels:
    l = int(label[1:], 16)
    if l < start_adr or l > end_adr:
        # print(f"{label} = ${l:04x}")
        outfile.write(f"{label} = ${l:04x}\n")

for line in disasmd_lines:
    dl_label = line.split(" ")[0]
    dl_rest = line.split(" ", 1)[1]

    if dl_label in labels:
        # print(line)
        outfile.write(f"{line}\n")
    else:
        # print(f"      {dl_rest}")
        outfile.write(f"      {dl_rest}\n")
outfile.close()

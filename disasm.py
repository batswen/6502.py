from Const import *
import json

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

# source = [0xa9, 0x00, 0x8d, 0x20, 0xd0, 0xb1, 0x64, 0x10, 0x02, 0x30, 0xfc, 0x60]

# source = [0x78, 0xa9, 0x12, 0x8d, 0x14, 0x03, 0xa9, 0xc0, 0x8d, 0x15, 0x03, 0xa9, 0x93, 0x20, 0xd2, 0xff, 0x58, 0x60, 0x4c, 0x31, 0xea]

json_file = open("basic.json")
json_data = json_file.read()
json_file.close()

data = json.loads(json_data)

source_file = open(data["filename"], "rb")
source = source_file.read()
source_file.close()

byte_table = data["byte_table"]
word_table = data["word_table"]

dis_opcodes = [None for x in range(255)]

for op in OPCODES.keys():
    keys = OPCODES[op].keys()
    for key in keys:
        dis_opcodes[OPCODES[op][key]] = { "monic": op, "addressing_mode": key }

start_adr = int(data["start"], 16)
index = 0
if data["first_two_bytes_are_start"]: #untested
    start_adr -= 2
    index = 2

while index < len(source) and index < 1000:
    address = start_adr + index
    b = source[index]

    if is_byte(address):
        if b >= 32 and b <= 122:
            print(f'{address:04x} {b:02x}       .by ${b:02x}   ; "{chr(b)}"')
        elif b in (8, 10, 13):
            c = [0,1,2,3,4,5,6,7, "Backspace",9,"Line feed (\\r)",0xb,0xc,"Carriage return (\\n)"][b]
            print(f'{address:04x} {b:02x}       .by ${b:02x}   ; "{c}"')

        #
        elif b >= 65 + 128 and b <= 90 + 128 or b == 35 + 128: # "a"-"z", "#"
            print(f'{address:04x} {b:02x}       .by ${b:02x}   ; "{chr(b)}" / "{chr(b - 128)}"')
        else:
            print(f'{address:04x} {b:02x}       .by ${b:02x}')
        index += 1
        continue

    if is_word(address):
        print(f'{address:04x} {b:02x} {source[index + 1]:02x}    .wo ${source[index + 1]:02x}{b:02x}')
        index += 2
        continue

    if dis_opcodes[b] == None:
        print(f"{address:04x} {b:02x}       ???")
        index += 1
        continue

    adr_mode = dis_opcodes[b]["addressing_mode"]
    monic = dis_opcodes[b]["monic"]
    # if adr in byte, word, text ...

    if adr_mode == IMPLIED:
        print(f"{address:04x} {b:02x}       {monic}")
    elif adr_mode == RELATIVE: # !!!
        distance = source[index + 1]
        b_adress = address + distance + 2
        if distance > 127:
            b_adress = address + distance - 254

        print(f"{address:04x} {b:02x} {source[index + 1]:02x}    {monic} ${b_adress:02x}")
    elif adr_mode == ZP:
        print(f"{address:04x} {b:02x} {source[index + 1]:02x}    {monic} ${source[index + 1]:02x}")
    elif adr_mode == ZPX:
        print(f"{address:04x} {b:02x} {source[index + 1]:02x}    {monic} ${source[index + 1]:02x},x")
    elif adr_mode == ZPY:
        print(f"{address:04x} {b:02x} {source[index + 1]:02x}    {monic} ${source[index + 1]:02x},y")
    elif adr_mode == USELESS:
        print(f"{address:04x} {b:02x} {source[index + 1]:02x}    {monic} (${source[index + 1]:02x},x)")
    elif adr_mode == INDIRECTY:
        print(f"{address:04x} {b:02x} {source[index + 1]:02x}    {monic} (${source[index + 1]:02x}),y")
    elif adr_mode == IMMEDIATE:
        print(f"{address:04x} {b:02x} {source[index + 1]:02x}    {monic} #${source[index + 1]:02x}    ;{source[index + 1]}")
    elif adr_mode == ABSOLUTE:
        print(f"{address:04x} {b:02x} {source[index + 1]:02x} {source[index + 2]:02x} {monic} ${source[index + 2]:02x}{source[index + 1]:02x}")
    elif adr_mode == ABSOLUTEX:
        print(f"{address:04x} {b:02x} {source[index + 1]:02x} {source[index + 2]:02x} {monic} ${source[index + 2]:02x}{source[index + 1]:02x},x")
    elif adr_mode == ABSOLUTEY:
        print(f"{address:04x} {b:02x} {source[index + 1]:02x} {source[index + 2]:02x} {monic} ${source[index + 2]:02x}{source[index + 1]:02x},y")
    elif adr_mode == INDIRECT:
        print(f"{address:04x} {b:02x} {source[index + 1]:02x} {source[index + 2]:02x} {monic} (${source[index + 2]:02x}{source[index + 1]:02x})")
    index += 1
    if adr_mode >= RELATIVE:
        index += 1
    if adr_mode >= ABSOLUTE:
        index += 1
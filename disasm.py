from Const import *

source = [0xa9, 0x00, 0x8d, 0x20, 0xd0, 0xb1, 0x64, 0x10, 0x02, 0x30, 0xfc, 0x60]

source = [0x78, 0xa9, 0x12, 0x8d, 0x14, 0x03, 0xa9, 0xc0, 0x8d, 0x15, 0x03, 0xa9, 0x93, 0x20, 0xd2, 0xff, 0x58, 0x60, 0x4c, 0x31, 0xea]

# source_file = open("basic.rom", "rb")
# source = source_file.read()
# source_file.close()

dis_opcodes = [None for x in range(255)]

for op in OPCODES.keys():
    keys = OPCODES[op].keys()
    for key in keys:
        dis_opcodes[OPCODES[op][key]] = {
            "monic": op, "addressing_mode": key
        }

start_adr = 0xc000
index = 0
while index < len(source) and index < 100:
    b = source[index]
    if dis_opcodes[b] == None:
        index += 1
        continue
    adr_mode = dis_opcodes[b]["addressing_mode"]
    monic = dis_opcodes[b]["monic"]
    # if adr in byte, word, text ...
    if adr_mode == IMPLIED:
        print(f"{start_adr + index:04x} {b:02x}       {monic}")
    elif adr_mode == RELATIVE: # !!!
        distance = source[index + 1]
        b_adress = start_adr + index + distance + 2
        if distance > 127:
            b_adress = start_adr + index + distance - 254

        print(f"{start_adr + index:04x} {b:02x} {source[index + 1]:02x}    {monic} ${b_adress:02x}")
    elif adr_mode == ZP:
        print(f"{start_adr + index:04x} {b:02x} {source[index + 1]:02x}    {monic} ${source[index + 1]:02x}")
    elif adr_mode == ZPX:
        print(f"{start_adr + index:04x} {b:02x} {source[index + 1]:02x}    {monic} ${source[index + 1]:02x},x")
    elif adr_mode == ZPY:
        print(f"{start_adr + index:04x} {b:02x} {source[index + 1]:02x}    {monic} ${source[index + 1]:02x},y")
    elif adr_mode == USELESS:
        print(f"{start_adr + index:04x} {b:02x} {source[index + 1]:02x}    {monic} (${source[index + 1]:02x},x)")
    elif adr_mode == INDIRECTY:
        print(f"{start_adr + index:04x} {b:02x} {source[index + 1]:02x}    {monic} (${source[index + 1]:02x}),y")
    elif adr_mode == IMMEDIATE:
        print(f"{start_adr + index:04x} {b:02x} {source[index + 1]:02x}    {monic} #${source[index + 1]:02x}    ;{source[index + 1]}")
    elif adr_mode == ABSOLUTE:
        print(f"{start_adr + index:04x} {b:02x} {source[index + 1]:02x} {source[index + 2]:02x} {monic} ${source[index + 2]:02x}{source[index + 1]:02x}")
    elif adr_mode == ABSOLUTEX:
        print(f"{start_adr + index:04x} {b:02x} {source[index + 1]:02x} {source[index + 2]:02x} {monic} ${source[index + 2]:02x}{source[index + 1]:02x},x")
    elif adr_mode == ABSOLUTEY:
        print(f"{start_adr + index:04x} {b:02x} {source[index + 1]:02x} {source[index + 2]:02x} {monic} ${source[index + 2]:02x}{source[index + 1]:02x},y")
    elif adr_mode == INDIRECT:
        print(f"{start_adr + index:04x} {b:02x} {source[index + 1]:02x} {source[index + 2]:02x} {monic} (${source[index + 2]:02x}{source[index + 1]:02x})")
    index += 1
    if adr_mode >= RELATIVE:
        index += 1
    if adr_mode >= ABSOLUTE:
        index += 1
#! /usr/bin/python
import sys
import re

def array2buff(array):
        buff = ":"
        checksum = 0
        for pos in range(len(array)):
                dd = array[pos]
                checksum = (checksum + dd)%256
                buff = buff + "{:02X}".format(dd)

        checksum = ( - checksum)%256
        buff = buff + "{:02X}".format(checksum)
        return buff

def buff2array(buff):
        array = []
        for pos in range(len(buff)//2):
                dd = buff[pos*2:pos*2+2]
                array.append(int(dd,16))

        return array

r_02line = re.compile(":02000002")
r_00line = re.compile(":......00")
r_03line = re.compile(":04000003")
r_04line = re.compile(":04000004")
r_05line = re.compile(":04000005")
r_ffline = re.compile(":00000001FF")
r_doseol = re.compile("\r\n\Z")
doseol = "\r\n"
unixeol = "\n"

addr_offset = 0
addr_high = 0
last_high = -1

for line in sys.stdin:
        if r_doseol.search(line):
                eol = doseol
                codelen = len(line) - 3
        else:
                eol = unixeol
                codelen = len(line) - 2

        buff = ":"
        checksum = 0

        if  r_02line.match(line):
                addr = int(line[9:13],16)*16
                buff_array = [2,0,0,4,0,addr//65536]
                addr_offset = addr
                addr_high = addr//65536

                buff = array2buff(buff_array)
                # print buff+eol,

        elif r_05line.match(line):
                addr = int(line[9:13],16)*4096 + int(line[13:17],16)
                buff_array = [2,0,0,5,addr//16777216,addr%16777216//65536,addr%65536//256,addr%256]

                buff = array2buff(buff_array)
                # print buff+eol,

        elif r_03line.match(line):
                addr = int(line[9:13],16)*16 + int(line[13:17],16)
                buff_array = [2,0,0,5,addr//16777216,addr%16777216//65536,addr%65536//256,addr%256]

                buff = array2buff(buff_array)
                # print buff+eol,

        elif r_04line.match(line):
                addr = int(line[9:13],16)*65536
                buff_array = [2,0,0,4,0,addr//65536]
                addr_offset = addr
                addr_high = addr//65536

                buff = array2buff(buff_array)
                print buff+eol,

        elif r_00line.match(line):
                # print line,
                codelen = (int(line[1:3],16)+4)*2
                addr = addr_offset + int(line[3:7],16)
                addr_high = addr//65536
                if ( addr_high <> last_high ) :
                        buff_array = [2,0,0,4,0,addr//65536]
                        buff = array2buff(buff_array)
                        last_high = addr_high
                        print buff+eol,

                buff_array = buff2array(line[1:codelen+1])
                buff_array[1] = addr%65536//256
                buff_array[2] = addr%65536%256
                buff = array2buff(buff_array)
                print buff+eol,

        elif r_ffline.match(line):
                "dummy"

        else:
                print line,

print ":00000001FF"+eol,

from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

def checksum(str_):
    str_ = bytearray(str_)
    csum = 0
    countTo = (len(str_) // 2) * 2

    for count in range(0, countTo, 2):
        thisVal = str_[count + 1] * 256 + str_[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff

    if countTo < len(str_):
        csum = csum + str_[-1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        #accessing icmp header from packet
        icmpHeader = recPacket[20:28]
        icmpType, code, mychecksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)

        #verify the ID of packet
        if icmpType != 8 and packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

        timeLeft = timeLeft - howLongInSelect

        if timeLeft <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
        # Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = htons(myChecksum)

        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
        packet = header + data
        mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
        # Both LISTS and TUPLES consist of a number of objects
        # which can be referenced by their position number within the object


def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    # Create Socket here
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF #Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    pings = 0
    # Send ping requests to a server separated by approximately one second
    while pings < 5:
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)
        pings += 1
    return delay

if __name__ == "__main__":
    # Picked IP of different continent from:
    # https://www.dotcom-monitor.com/blog/technical-tools/network-location-ip-addresses/
    print("Pinging London (United Kingdom)")
    ping("5.152.197.179")

    print('-----------------------')
    print("Pinging Johannesburg (South Africa)")
    ping("197.221.23.194") #china

from socket import *

msg = "\r\n I love Computer Networks!"
endmsg = "\r\n.\r\n"

mailserver = ("smtp.mail.yahoo.com", 587) #Fill in start #Fill in end

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)


recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
 print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'helo Damien\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
 print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFrom = "MAIL FROM:<myemail@yahoo.com>\r\n"
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv1[:3] != '250':
 print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptTo = "RCPT TO:<rcptemail>\r\n"
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv1[:3] != '250':
 print('250 reply not received from server.')

# Send DATA command and print server response.
data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv1[:3] != '250':
 print('250 reply not received from server.')

# Send message data.
message = input("Enter message: \r\n")

# Message ends with a single period

clientSocket.send((message + endmsg).encode())
print(recv1)
if recv1[:3] != '250':
 print('250 reply not received from server.')

# Send QUIT command and get server response.
clientSocket.send("QUIT\n".encode())
message = clientSocket.recv(1024).decode()
print(message)
clientSocket.close()
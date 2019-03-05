import bluetooth 

hostMACAddress = '4C:BB:58:BE:BE:79'
port = 3 
backlog = 1
size = 4096
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
print("Waiting for connection")
try:
	client, clientInfo = s.accept()
	print("Connected")
	while 1:
		data = client.recv(size)
		if data:
			print(data.decode('UTF-8'))
			client.send(data)
except:	
	print("Closing socket")
	client.close()
	s.close()

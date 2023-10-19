import	socketserver
import Encryption

class	MyTCPHandler(socketserver.BaseRequestHandler):
    def	handle(self):
        #	self.request	is	the	TCP	socket	connected	to	the	client
        self.data	=	self.request.recv(1024).strip()
        print("{}	sent message:	".format(self.client_address[0]))
        print(self.data)
        self.data = str(Encryption.cipher.decrypt(self.data))
        print(self.data)

if __name__  ==	"__main__":
    try:
        HOST,	PORT	=	"localhost",	9999
        #	Create	the	server,	binding	to	localhost	on	port	9999
        server	=	socketserver.TCPServer((HOST,	PORT),	MyTCPHandler)
        # Activate	the	server;	this	will	keep	running	until	you
        #	interrupt	the	program	with	Ctrl-C
        server.serve_forever()
    except server.error as e:
        print("Error:",e)
        exit(1)
    finally:
        server.close()

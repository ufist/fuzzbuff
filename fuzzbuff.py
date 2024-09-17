import socket
import sys
import argparse
import select
import subprocess
import time

bad = '\033[91m[-]\033[0m'
good = '\033[92m[+]\033[0m'
info = '\033[94m[*]\033[0m'
error = '\033[91m[E]\033[0m'
end = '\r\n'

def getH():
	print(info,"Please specify the Host and Port")
	host = input("() Host: ")
	port = input("() Port: ")
	return host,port

def receive(sock):
	sock.setblocking(0)
	ready = select.select([sock], [], [], 10)
    
	if ready[0]:
		try:
			data = sock.recv(1024)
			print(info, f"Socket data received: {data}")
		except socket.error as e:
			print(error,f"{e}")
	else:
		print(info, "Nothing received, continuing anyway")

def spattern(host, port, pattern, prefix):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, port))
		print(info,"Sending pattern...")
		s.send(prefix.encode() + pattern.encode() + end.encode())
		if not nw:
			print(info,"Attempting to receive any banners (10s)...")
			receive(s)
		print(good,"Pattern sent!")
		sys.exit()
	except Exception as e:
		print(error,f"{e}")

def fuzzF(host, port, startf, endf, delay, char, pattern, prefix, nw):
	if char and startf > 0 and endf > 0 and delay > 0:
		pass
	elif pattern:
		pass
	else:
		print(error,"Character, End and Start Value required!")
	if pattern:
		print(info,"Creating pattern...")
		result = subprocess.run(["msf-pattern_create", "-l", str(pattern)], capture_output=True, text=True)
		patternO = result.stdout
		spattern(host,port,patternO,prefix)
	else:
		pass
	try:
		print("Start Value:",startf,"End Value:",endf,"Delay:",delay,"Character:",char,"Prefix:",prefix)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, port))
		if not nw:
			print(info,"Attempting to receive any banners (10s)...")
			receive(s)
		fuzz = startf
		while fuzz < endf:
			print(good,fuzz)
			payload = prefix.encode()
			payload += char.encode() * fuzz
			payload += end.encode()
			s.send(payload)
			if not nw:
				receive(s)
			fuzz += startf
			time.sleep(delay)
	except Exception as e:
		print(error,f"{e}")

def main():
	parser = argparse.ArgumentParser(description="Fuzzing script with socket connection.")
	parser.add_argument("host", help="Target host IP address")
	parser.add_argument("port", type=int, help="Target port number")
	parser.add_argument("-s", "--start", type=int, default=1000, help="Starting fuzz value")
	parser.add_argument("-e", "--end", type=int, default=1000000, help="Ending fuzz value")
	parser.add_argument("-d", "--delay", type=float, default=0.5, help="Delay between fuzzing attempts")
	parser.add_argument("-c", "--char", default="A", help="Character to send in fuzzing")
	parser.add_argument("-p", "--pattern", type=int, help="Send MSF Pattern, specify length")
	parser.add_argument("-x", "--prefix", default="", help="Prefix before fuzz payload (MAKE SURE TO ADD SPACE IF NEEDED) [Ex: -x 'USER ']")
	parser.add_argument("-n", "--no-receive", action="store_true", help="Do not attempt to receive any response from the host")

	args = parser.parse_args()

	startf = args.start
	endf = args.end
	delay = args.delay
	char = args.char
	pattern = args.pattern
	prefix = args.prefix
	nw = args.no_receive
	try:
		host = args.host
		port = args.port
		fuzzF(host, port, startf, endf, delay, char, pattern, prefix, nw)
	except Exception as e:
		print(error, f"{e}")

if __name__ == "__main__":
	main()

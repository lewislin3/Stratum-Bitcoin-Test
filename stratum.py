import socket
import json
import binascii
import hashlib
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("stratum.antpool.com", 3333))

sock.send("""{"id": 1, "method": "mining.subscribe", "params": []}\n""")
sub_data = sock.recv(4000)
print (sub_data)
sub_data = json.loads(sub_data)
extranonce1 = sub_data['result'][1]

sock.send("""{"params": ["lewislin3.123","x"], "id":2, "method": "mining.authorize"}\n""")
work = sock.recv(4000)
print (work.split("\n")[0])
diff = json.loads(work.split("\n")[0])
print(diff['params'])

task = json.loads(work.split("\n")[1])

job_id = task['params'][0]
print ("job id ",job_id)
prehash = task['params'][1]
print ("prehash",prehash)
coinb1 = task['params'][2]
print ("coinbase1",coinb1)
coinb2 = task['params'][3]
print ("coinbase2",coinb2)
merkle_branch = task['params'][4]
print ("merkle branch",merkle_branch)
version = task['params'][5]
print ("version",version)
nbits = task['params'][6]
print ("nbits",nbits)
ntimes = task['params'][7]
print ("ntimes",ntimes)
clean_jobs = task['params'][8]
print ("clean jobs",clean_jobs)


for extra2 in xrange(0, 0x7fffffff):

	extranonce2 = struct.pack('<I', extra2)


	#merkle root
	coinbase = coinb1 + extranonce1 + extranonce2 + coinb2
	hashbase = hashlib.sha256(coinbase).hexdigest()
	for i in merkle_branch:	
		#print(i)
		byte = hashbase + i
		hashbase = hashlib.sha256(coinbase).hexdigest()
		
		merkle_root = hashbase
	print("merkle root", merkle_root)


	#swap version :nversion
	nversion=""
	for x in range(-1, -len(version), -2):
		nversion += version[x-1] + version[x]


	#swap prehash :nprehash
	nprehash = list(prehash)
	lens=len(prehash)
	for x in range(0,lens,8):

		nprehash[x]=prehash[x+6]
		nprehash[x+1]=prehash[x+7]
		nprehash[x+2]=prehash[x+4]
		nprehash[x+3]=prehash[x+5]
		nprehash[x+4]=prehash[x+2]
		nprehash[x+5]=prehash[x+3]
		nprehash[x+6]=prehash[x+0]
		nprehash[x+7]=prehash[x+1]
	nprehash = ''.join(nprehash)


	#swap ntime :nntime
	nntime=""
	for x in range(-1, -len(ntimes), -2):
		nntime += ntimes[x-1] + ntimes[x]


	#swap nbits :nnbits
	nnbits=""
	for x in range(-1, -len(nbits), -2):
		nnbits += nbits[x-1] + nbits[x]


	header_prefix = nversion + nprehash + merkle_root + nntime + nnbits
	print("header prefix", header_prefix)
	
	for n in xrange(0,0x7fffffff, 1):
		nonce = struct.pack('<I', n)
		pow = sha256(header_prefix+nonce)[::-1].encode('hex')
		


		

#coinbase = bin(int(binascii.hexlify(coinbase),16))
#print (coinbase)

'''

	
nonce="00007f8a"
nnonce=""
for x in range(-1, -len(nonce), -2):
	nnonce += nonce[x-1] + nonce[x]
print("reverse nonce",nnonce)


time = list(ntimes)
time[7]="d"
time = ''.join(time)
print(time)

bytestream = nversion + nprehash + hashbase + nntime + nnbits + "00000000"
print (bytestream)
bytestream = bin(int(binascii.hexlify(bytestream),16))
bytestream = hashlib.sha256(bytestream).hexdigest()

print("bytestream", bytestream)

'''


import socket
import json
import binascii
import hashlib
import struct
import time
import threading


def sha256d(instr):
	instr = instr.decode('hex')
	instr =  (hashlib.sha256(hashlib.sha256(instr).digest()).digest()).encode('hex_codec')
	return instr

def is_json(myjson):
	try:
		json_object = json.loads(myjson)
	except ValueError, e:
		return False
	return True

def working(job_id ,prehash, coinb1, coinb2, merkle_branch, version, nbits, ntimes, clean_jobs, difficult, sock ):
	start=time.time()
	print(sock)
	number=0
	extranonce2="00000001"
	
	#merkle root
	coinbase = coinb1 + extranonce1 + extranonce2 + coinb2
	hashbase = sha256d(coinbase)

	merkle_root = hashbase
	for i in merkle_branch:	
		a=i.encode('ascii','ignore')
		byte = hashbase + a
		byte = sha256d(byte)
		merkle_root = byte

	nmr = list(merkle_root)
	lens=len(merkle_root)
	for x in range(0,lens,8):

		nmr[x]=merkle_root[x+6]
		nmr[x+1]=merkle_root[x+7]
		nmr[x+2]=merkle_root[x+4]
		nmr[x+3]=merkle_root[x+5]
		nmr[x+4]=merkle_root[x+2]
		nmr[x+5]=merkle_root[x+3]
		nmr[x+6]=merkle_root[x+0]
		nmr[x+7]=merkle_root[x+1]

	nmr = ''.join(nmr)

	#merkle_root = "".join(reversed([merkle_root[i:i+2] for i in range(0, len(merkle_root), 2)]))
	header_prefix = version + prehash + nmr + ntimes + nbits 
	
	for n in xrange(0,0x000fffff):
		
		nonce=str(hex(n))[2:]
		nonce=nonce.zfill(8)
		header_prefix = header_prefix + nonce + "000000800000000000000000000000000000000000000000000000000000000000000000000000000000000080020000"
		header_prefix = sha256d(header_prefix)
		
		hp=int(header_prefix,16)
		#print(n)

		if hp<difficult:
			ans="{\"params\":[\"lewislin3.123\", \"" + job_id + "\", \"" + extranonce2 + "\", \"" + ntimes + "\", \"" + nonce + "\"], \"id\": 4, \"method\": \"mining.submit\"}\n"
			print(ans)
			print(header_prefix)
			sock.send(ans)
			
		number = number+1
	print ((time.time()-start))




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("stratum.antpool.com", 3333))
sock.send("""{"id": 1, "method": "mining.subscribe", "params": []}\n""")
sock.send("""{"params": ["lewislin3.123","x"], "id":2, "method": "mining.authorize"}\n""")
while True:
	work = sock.recv(4000)
	print(work)
	work = work.split("\n")
	
	for split_work in work:
		if is_json(split_work):
			now_split_work = json.loads(split_work)
			# check whether is a work to do or a simple output
			if now_split_work['id']==1:
				extranonce1 = now_split_work['result'][1]

			if 'method' in now_split_work.keys():

				#setting difficulty
				if now_split_work['method']=="mining.set_difficulty":
					difficult = now_split_work['params'][0]
					print ("diff",difficult)
					a=0x0000FFFF00000000000000000000000000000000000000000000000000000000
					difficult=a/difficult

				#doing work
				if now_split_work['method']=="mining.notify":
					#print(now_split_work)
					job_id = now_split_work['params'][0]
					#print("job id",job_id)
					prehash = now_split_work['params'][1]
					coinb1 = now_split_work['params'][2]
					coinb2 = now_split_work['params'][3]
					merkle_branch = now_split_work['params'][4]
					version = now_split_work['params'][5]
					nbits = now_split_work['params'][6]
					ntimes = now_split_work['params'][7]
					clean_jobs = now_split_work['params'][8]
					working(job_id ,prehash, coinb1, coinb2, merkle_branch, version, nbits, ntimes, clean_jobs, difficult, sock )

					






		#print("header_prefix",header_prefix)
		# in FPGA hash and check diff
		# if ok ->mining submit



		
	
		

		


		


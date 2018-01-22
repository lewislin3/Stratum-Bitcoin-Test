import socket
import json
import binascii
import hashlib
import struct
import time
import threading

def working(job_id ,prehash, coinb1, coinb2, merkle_branch, version, nbits, ntimes, clean_jobs,difficult ):

	global threadnum

	for extra2 in xrange(0, 0x0000ffff):

		start=time.time()
		number=0
		extranonce2=str(hex(extra2))[2:]
		extranonce2=extranonce2.zfill(8)
		


		#merkle root
		coinbase = coinb1 + extranonce1 + extranonce2 + coinb2
		coinbase = coinbase.decode('hex')
		#FPGA double hash=>hashase
		hashbase = (hashlib.sha256(hashlib.sha256(coinbase).digest()).digest()).encode('hex_codec')

		merkle_root = hashbase
		for i in merkle_branch:	
			a=i.encode('ascii','ignore')
			byte = hashbase + a
			byte = byte.decode('hex')
			byte = (hashlib.sha256(hashlib.sha256(byte).digest()).digest()).encode('hex_codec')
			merkle_root = byte



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
	
		for n in xrange(0,0x0000ffff):
		
			nonce=str(hex(n))[2:]
			nonce=nonce.zfill(8)
			header_prefix = header_prefix+nonce
			header_prefix = (hashlib.sha256(hashlib.sha256(header_prefix).digest()).digest()).encode('hex_codec')
			hp="".join(reversed([header_prefix[i:i+2] for i in range(0, len(header_prefix), 2)]))
			hp=int(hp,16)
			#print(n)

			if hp<difficult:
				ans="{\"params\":[\"lewislin3.123\", \"" + job_id + "\", \"" + extranonce2 + "\", \"" + ntime + "\", \"" + nonce + "\"], \"id\": 4, \"method\": \"momomg.submit\"}"
				print ans
				print header_prefix
				sock.send(ans)
				print sock.recv(4000)
			number = number+1
		print number/(time.time()-start)
		threadnum -= 1


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("stratum.antpool.com", 3333))

sock.send("""{"id": 1, "method": "mining.subscribe", "params": []}\n""")
sub_data = sock.recv(4000)
sub_data = json.loads(sub_data)
extranonce1 = sub_data['result'][1]
sock.send("""{"params": ["lewislin3.123","x"], "id":2, "method": "mining.authorize"}\n""")

global threadnum
threadnum=0
while True:
	work = sock.recv(4000)
	print(work)
	work = work.split("\n")
	
	for split_work in work:
		if split_work != "":
			now_split_work = json.loads(split_work)
			# check whether is a work to do or a simple output
			if 'method' in now_split_work.keys():

				#setting difficulty
				if now_split_work['method']=="mining.set_difficulty":
					difficult = now_split_work['params'][0]
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
					working(job_id ,prehash, coinb1, coinb2, merkle_branch, version, nbits, ntimes, clean_jobs,difficult )
					threadnum += 1
					






		#print("header_prefix",header_prefix)
		# in FPGA hash and check diff
		# if ok ->mining submit



		
	
		

		


		


from Crypto.Util import number
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-k", "--keysize", type=int, help="Bit size for keys to be generated(P1, P2, & P3).")
arg_parser.add_argument("keyfile", help="File name to store keys in.")
arg_parser.add_argument("-e", "--encrypt", action="append", help="Encrypt message.")
arg_parser.add_argument("-d", "--decrypt", type=int, help="Decrypt a cipher.")
arg_parser.add_argument("-b", "--both", type=int, help="Both encrypt and decrypt a message.")
arg_parser.add_argument("-a", "--addition", action="store_true", help="Homomorphic addition")

def generate_key(key_length):
	p1 = 0
	p2 = 0 
	Q = 0
	p3 = number.getPrime(key_length)
	while True:
		p1 = number.getPrime(key_length)
		Q = 2*p1 + 1
		if number.isPrime(Q):
			p2 = number.getPrime(key_length)
			break
	N = p1*p2
	T = Q*p3
	h = []
	while len(h) < 2:
		random = number.getRandomInteger(key_length)
		if random not in h:
			h.append(random)
	g = [str(pow(x,(2*(p3-1)),T)) for x in h] #pow(x,y,z) returns x to the power y modulo z.
	key = "{0}\n{1}\n{2}\n{3}".format(N, p1, str(','.join(g)), T)
	return key


def get_keys_from_file(keyfile):
    keys = []
    with open(keyfile, 'r') as f:
    	for key in f:
    		if ',' in key:
    			split_key = key.split(',')
    			for x in split_key:
    				keys.append(int(x))
    		else:
    			keys.append(int(key))
    return keys

def encrypt(message, keys):
	r = number.getRandomInteger(len(str(keys[0]))-1)
	return pow((r*keys[1] + message), 1, keys[0]) 


def decrypt(cipher, keys):
	return pow(cipher, 1, keys[1])


def parse_args():
	args = arg_parser.parse_args()
	# Generate keys and save if keysize and keyfile are provided.
	if args.keysize is not None:
		key_size = args.keysize
		print("Generating keys for keysize: {0}".format(key_size))
		if args.keyfile:
			with open(args.keyfile, 'w') as file:
				file.write(generate_key(key_size))
			print("Generated keys successfully!")
	elif args.addition:
		if args.encrypt:
			m1 = int(args.encrypt[0])
			m2 = int(args.encrypt[1])
			keys = get_keys_from_file(args.keyfile)
			print(pow(encrypt(m1+m2, keys),1,keys[0]))
		else:
			c1, c2 = args.addition.split()
			print(c1)
	elif args.encrypt:
		m = int(args.encrypt)
		keys = get_keys_from_file(args.keyfile)
		print(encrypt(m, keys))
	elif args.decrypt:
		cipher = args.decrypt
		keys = get_keys_from_file(args.keyfile)
		print(decrypt(cipher, keys))
	elif args.both:
		message = args.both
		keys = get_keys_from_file(args.keyfile)
		print(message)
		enc = encrypt(message, keys)
		print(enc)
		print(decrypt(enc, keys))
			

if __name__ == '__main__':
	parse_args()


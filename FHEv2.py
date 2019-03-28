from Crypto.Util import number
import sys


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


def test_equality(c1, c2, keys):
	equal = False
	gi = [keys[2], keys[3]]
	for x in gi:
		power = abs(c1-c2)
		left = pow(x, power, keys[4])
		right = pow(1,1,int(keys[4]))
		equal = (left == right)
	return equal


def get_ciphers_from_args(args, keys):
	i = 2
	ciphers = []
	while (i < len(args)-1):
		if '-e' in args[i]:
			ciphers.append(encrypt(int(args[i+1]), keys))
			i = i + 2
		else:
			ciphers.append(int(args[i]))
			i = i + 1
	return ciphers


def parse_args(args):
	if '-k' in args[1]:
		key_size = int(args[2])
		with open(args[3], 'w') as file:
			file.write(generate_key(key_size))
		print("Generated keys successfully!")
	elif '-e' in args[1]:
		m = int(args[2])
		keys = get_keys_from_file(args[3])
		print(encrypt(m, keys))
	elif '-d' in args[1]:
		cipher = int(args[2])
		keys = get_keys_from_file(args[3])
		print(decrypt(cipher, keys))
	elif '-a' in args[1]:
		keys = get_keys_from_file(args[len(args)-1])
		ciphers = get_ciphers_from_args(args, keys)
		print(pow( (ciphers[0] + ciphers[1]),1,keys[0]))
	elif '-m' in args[1]:
		keys = get_keys_from_file(args[len(args)-1])
		ciphers = get_ciphers_from_args(args, keys)
		print(pow( (ciphers[0] * ciphers[1]),1,keys[0]))
	elif '-t' in args[1]:
		keys = get_keys_from_file(args[len(args)-1])
		ciphers = get_ciphers_from_args(args, keys)
		print(test_equality(ciphers[0], ciphers[1], keys))
			

if __name__ == '__main__':
	parse_args(sys.argv)


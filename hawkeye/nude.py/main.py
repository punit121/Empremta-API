import nude
from nude import Nude
import sys
def main(url):
	

	x=nude.is_nude(url)

	#n = Nude('examples/images/test2.jpg')
	#n.parse()
	#print("Nudity result :", n.result, n.inspect())
	print(x)

	f = open('data.txt', 'r+')
	f.truncate()
	with open('data.txt', 'w') as outfile:      
		outfile.write(str(x))

	return(1)	


if __name__ == '__main__':

	url=sys.argv[1]
	main(url)	
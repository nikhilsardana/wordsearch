import sys
import re
import codecs

args = len(sys.argv) - 1
numchar = 0

if(args!=1):
	print("This script requires one argument: number of characters per row.")
	sys.exit(2)
elif (args==1):
	try:
		numchar = int(sys.argv[1])
		if(numchar<=0):
			print("Please input a positive integer.")
			sys.exit(2)
	except ValueError:
		print("Please input a valid integer.")
		sys.exit(2)

print(numchar)

with open("input.txt") as f:
	letters = f.readlines()

letters = [x.strip() for x in letters]
letters = ''.join(letters)
letters = ''.join(letters.split())

formatted = re.sub("(.{%d})"%numchar, "\\1\n", letters, 0, re.DOTALL)
print(formatted)

f = open("formatted.txt", "w")
f.write(formatted)
f.close()

print("You can now run wordsearch.py.")
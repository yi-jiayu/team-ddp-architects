t= "RRRRRRTTTTYYYULLL"

def RLE2(inp):
	last = inp[0]
	output=0
	count=1
	# check=""
	for i in range(1,len(inp)):
		cur = inp[i]
		if cur!=last:
			# check+=str(count)+last
			if count>9:
				output+=3
			elif count>99:
				output+=4
			elif count>1:
				output+=2
			else:
				output+=1
			count=1

		else:
			count+=1

		last=cur
		if i==len(inp)-1:
			if count>9:
				output+=3
			elif count>99:
				output+=4
			elif count>1:
				output+=2
			else:
				output+=1
			# check+=str(count)+last
	# print(check)
	return output*8


def findord(inp):
	summ =0
	for i in inp:
		summ+=ord(i)
	return summ

def LZW(inp):
	p = inp[0]
	d={}
	count=256
	output=0
	for i in range(1,len(inp)):
		c=inp[i]
		temp = p+c
		if temp in d:
			p += c
		else:
			d[temp]=count
			count+=1
			output += 1
			p = c

	return output*12

t2="BABAABAAA"
# print(LZW(t2))

def WDE(inp):
	cur = ""
	d={}
	non_alpha=0
	numWords=0
	for i in range(len(inp)):
		if inp[i].isalpha():
			cur +=inp[i]
		else:
			non_alpha +=1
			numWords+=1
			d[cur]=len(cur)*8
			cur=""
		# print('d',d)
		if i==len(inp)-1:
			numWords+=1

	dictSize = sum(d.values())
	# print('dictsize',dictSize)
	# print('numWords', numWords)
	return numWords*12 + non_alpha*12 + dictSize

t3="HOW MUCH WOOD COULD A WOOD CHUCK CHUCK IF A WOOD CHUCK COULD CHUCK WOOD"
# print(WDE(t3))

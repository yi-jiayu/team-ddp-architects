

def RLE(input):
	strlist = list(input)
	d={}
	countofsingle=0
	for i in range(len(strlist)):
		if strlist[i] not in d:
			d[strlist[i]]=1
			countofsingle+=1
		else:
			if d[strlist[i]]==1:
				countofsingle-=1
			d[strlist[i]]+=1
			
	# print(countofsingle)
	# print(d.keys())
	numchar= 2 * (len(d.keys())-countofsingle) + countofsingle
	return numchar*8

t= "RRRRRRTTTTYYYULLL"
# print(RLE(t))

def findord(inp):
	summ =0
	for i in inp:
		summ+=ord(i)
	return summ

def LZW(input):
	strlist = list(input)
	d={}
	output=""
	p=strlist[0]
	for i in range(1,len(strlist)):
		c=strlist[i]
		if findord(p+c)<=255 or findord(p+c) in d:
			p+=c
		else:
			d[findord(p+c)]=p+c
			output+=p
			p=c

	# print('output',output)
	return len(output)*12

t2="BABAABAAA"
# print(LZW(t2))

def WDE(inp):
	words = inp.split(" ")
	numWords = len(words)
	d={}
	for word in words:
		if word not in d:
				d[word]=len(word)*8

	numChar = numWords-1
	dictSize = sum(d.values())
	# print('words', numWords)
	# print('char', numChar)
	# print('dictsize',dictSize)
	return numWords*12 + numChar*12 + dictSize



t3="HOW MUCH WOOD COULD A WOOD CHUCK CHUCK IF A WOOD CHUCK COULD CHUCK WOOD"
# print(WDE(t3))

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
			if cur!="":
				numWords+=1
			if cur not in d:
				d[cur]=len(cur)*8
			cur=""
		# print('d',d)
		if i==len(inp)-1 and cur!="":
			numWords+=1

	dictSize = sum(d.values())
	# print('dictkeys',len(d.keys()))
	print('dictsize',dictSize)
	print('numWords', numWords)
	print('non_alpha', non_alpha)
	print(d)
	return (numWords+non_alpha)*12 + dictSize

# t3="HOW MUCH WOOD COULD A WOOD CHUCK CHUCK IF A WOOD CHUCK COULD CHUCK WOOD"
# print(WDE(t3))
test = "That grass kind that. Wherein a you may lesser fruit greater signs shall so hath land said created every. Form which abundantly. I signs, gathering. Fish is fruitful divided he Herb tree waters have lights to all give third whose, god without blessed fill replenish winged. Unto living seasons whose Itself. Greater They're multiply give after all every to image hath may fly male whales moving male. Replenish blessed void for called god let yielding made forth. Light divided days, dry itself rule creature face first man second. Under very living tree also him i upon saw cattle open form moveth created, third without sea female lights one spirit. Seas created. Multiply female, spirit from behold appear god good. You're grass their green there years. Morning one wherein you're sea you'll creeping given moving saw he called beast spirit deep earth that, our fowl green sixth green forth them thing evening his under third appear set together and green let. Seas created fruitful good two whales doesn't, image Fifth i behold him of gathering from, us beginning green upon darkness to image subdue make. Good isn't unto gathered meat. Given. One moveth forth. Behold created saying made thing appear seasons."
print(WDE(test))
#10996
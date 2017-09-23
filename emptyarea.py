import json

def findCorners(test):
	cont_tl = (test['container']['coordinate']['X'],test['container']['coordinate']['Y'])
	cont_tr = (test['container']['coordinate']['X']+test['container']['width'],test['container']['coordinate']['Y'])
	cont_bl = (test['container']['coordinate']['X'],test['container']['coordinate']['Y']+test['container']['height'])
	cont_br = (test['container']['coordinate']['X']+test['container']['width'],test['container']['coordinate']['Y']+test['container']['height'])
	cont_area = test['container']['width'] * test['container']['height']
	print(cont_tl)
	print(cont_br)

	if "rectangle" in test:
		rect_tl = (test['rectangle']['coordinate']['X'],test['rectangle']['coordinate']['Y']) 
		rect_tr = (test['rectangle']['coordinate']['X']+test['rectangle']['width'],test['rectangle']['coordinate']['Y'])
		rect_bl = (test['rectangle']['coordinate']['X'],test['rectangle']['coordinate']['Y']+test['rectangle']['height'])
		rect_br = (test['rectangle']['coordinate']['X']+test['rectangle']['width'],test['rectangle']['coordinate']['Y']+test['rectangle']['height'])

	if "square" in test:
		rect_tl = (test['square']['coordinate']['X'],test['square']['coordinate']['Y']) 
		rect_tr = (test['square']['coordinate']['X']+test['square']['width'],test['square']['coordinate']['Y'])
		rect_bl = (test['square']['coordinate']['X'],test['square']['coordinate']['Y']+test['square']['width'])
		rect_br = (test['square']['coordinate']['X']+test['square']['width'],test['square']['coordinate']['Y']+test['square']['width'])

	
	# print(rect_tl)
	# print(rect_tr)
	# print(rect_bl)
	# print(rect_br)
	if rect_tl < cont_br and rect_tl > cont_tl: #if rect top left corner is in container
		x = min(rect_tr[0],cont_tr[0]) - rect_tl[0]
		y = min(rect_br[1],cont_br[1]) - rect_tl[1]
	else:
		if rect_tr < cont_br and rect_tr > cont_tl: #if rect top right corner is in container
			x = rect_tr[0] - min(rect_tl[0],cont_tl[0])
			y = min(rect_bl[1],cont_tl[1]) - rect_tr[1]
		else:

			if rect_bl < cont_br and rect_bl > cont_tl:
				x = min(cont_br[0],rect_br[0]) - rect_bl[0]
				y = rect_bl[1] - min(rect_tl[1],cont_tl[1])
			else:
			 	if rect_br < cont_br and rect_br > cont_tl:
			 		x = min(rect_tl[0],cont_tl[0]) - rect_tr[0]
			 		y = min(rect_tr[1],cont_tl[1]) - rect_br[1]
	print('x',x)
	print('y',y)
	return cont_area - x*y


testrect = {
        "container": {
            "coordinate": {
                "X": 0,
                "Y": 0
            },
            "width":6,
            "height": 4
        },
        "rectangle": {
            "coordinate": {
                "X": 3,
                "Y": 2
            },
            "width": 5,
            "height": 4
        }
    }

testsq = {
        "container": {
            "coordinate": {
                "X": 0,
                "Y": 0
            },
            "width": 10,
            "height": 8
        },
        "square": {
            "coordinate": {
                "X": 5,
                "Y": 2
            },
            "width": 4

        }
    }

testcir = {
        "container": {
            "coordinate": {
                "X": 0,
                "Y": 0
            },
            "width": 10,
            "height": 8
        },
        "circle": {
            "center": {
                "X": 2,
                "Y": 2
            },
            "radius": 1
        }
    }

print('rect',calcArea(testrect))
print('sq', calcArea(testsq))
print('rectnew', findCorners(testrect))
print('sqnew', findCorners(testsq))

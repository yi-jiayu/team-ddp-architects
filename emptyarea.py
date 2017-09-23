import json
import math

def calcArea(test):
	# cont = (xmin, xmax, ymin, ymax)
    cont = (test['container']['coordinate']['X'], test['container']['coordinate']['X']+test['container']['width'], test['container']['coordinate']['Y'], test['container']['coordinate']['Y']+test['container']['height'])
    cont_area = test['container']['width'] * test['container']['height']
    if "rectangle" in test:
        child = (test['rectangle']['coordinate']['X'], test['rectangle']['coordinate']['X']+test['rectangle']['width'], test['rectangle']['coordinate']['Y'], test['rectangle']['coordinate']['Y']+test['rectangle']['height'])
    elif "square" in test:
        child = (test['square']['coordinate']['X'], test['square']['coordinate']['X']+test['square']['width'], test['square']['coordinate']['Y'], test['square']['coordinate']['Y']+test['square']['width'])
    elif "circle" in test:
        rad = test['circle']['radius']
        child = (test['circle']['center']['X']-rad, test['circle']['center']['X']+rad, test['circle']['center']['Y']-rad, test['circle']['center']['Y']+rad)
        x = min(cont[1],child[1]) - max(cont[0],child[0])
        y = min(cont[3],child[3]) - max(cont[2],child[2])
        if x == y:
            return cont_area - math.pi*rad**2
        else:
            return cont_area - cutCircle(rad,0.00001,x,y)

    x = min(cont[1],child[1]) - max(cont[0],child[0])
    y = min(cont[3],child[3]) - max(cont[2],child[2])
    if x>0 and y>0:
        return cont_area - x*y
    else:
        return cont_area


def divideCircle(r):
	dx = 0.1
	num = math.floor(r/dx)
	total = sum(range(num+1))
	return total*4*0.1**2

def cutCircle(r,unit,x,y):
    ind = 0
    numInDiameter = r*2/unit
    area=unit**2
    total = 0
    count = 1
    inner = 0
    while ind+unit < x:
        ind+=unit
        lowerbound = r-count*unit
        if lowerbound < y:
            total += min((y-lowerbound)//unit,count*2) * area
        # total += 2*area*count
        if ind>r:   
            count-=1
        else:
            count += 1

    return total

# print(cutCircle(5,0.0001,5,5))
# print(divideCircle(5))
# print(math.pi**2*5/4)
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

# print('rect',calcArea(testrect))
# print('sq',calcArea(testsq))
# print('cir',calcArea(testcir))
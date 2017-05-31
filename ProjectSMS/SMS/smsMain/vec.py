def vectorContains(tab,phrase):
	for each in tab:
		if(each == phrase):
			return 1
	return 0

def choiceFieldTupleContains(myTuple,phrase):
	for each in myTuple:
		if(each[1] == phrase):
			return 1
	return 0
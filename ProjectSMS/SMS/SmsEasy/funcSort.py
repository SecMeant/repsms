from operator import itemgetter
# All Invented By HLZ , execute by WindSpring 
# to generate dictionary you can use evrywhere you want to have polish signs substitiude by they intiger equvalen
# Use 'R' or 'r' to get rverse dictionary 
def makeVirtualTable(mode):
	_polishSignDict = {}
	_polishSignDictReverse = {}
	_letters =" aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźżAĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ-"
	_letOrd = ['00/', '01/', '02/', '03/', '04/', '05/', '06/', '07/', '08/', '09/', '10/', '11/', '12/', '13/', '14/', '15/', '16/', '17/', '18/', '19/', '20/', '21/', '22/', '23/', '24/', '25/',
				'26/', '27/', '28/', '29/', '30/', '31/', '32/', '33/', '34/', '35/', '36/', '37/', '38/', '39/', '40/', '41/', '42/', '43/', '44/', '45/', '46/', '47/', 
				'48/', '49/', '50/', '51/', '52/', '53/', '54/', '55/', '56/', '57/', '58/', '59/', '60/', '61/', '62/', '63/', '64/', '65/', '66/', '67/', '68/', '69/','70/','71/']
	for l , o in zip(_letters, _letOrd):
		_polishSignDict.update({l: o})
		_polishSignDictReverse.update({o: l})
	if mode is 'R' or mode is 'r':
		return _polishSignDictReverse
	else:
		return _polishSignDict

# to get encoded string use this fun, fun uses above dictionary
def codeString(word):
	encodedWord=""
	VirtualTable = makeVirtualTable(None) 
	for ch in word:
		try:
			encodedWord += VirtualTable[ch]
		except:
			encodedWord += '99/'
	return encodedWord

# to decode string use this fun, fun uses  above  reverse dictionary
def decodeString(word):
	decodedWord=""
	VirtualReverse = makeVirtualTable('R')

	i = 0
	j = 3
	while(i < len(word)):
		try:
			decodedWord += VirtualReverse[word[i:j]]
			i+=3
			j+=3
		except:
			decodedWord +='-'
	return decodedWord

# you can use this function only if you have date in this format [(),(),()...] or [[],[],[]...] 
# to sort polish signs
# fun takes two arguments
# table  <<-- all data you want to sort
# sort_id <<-- key of column you want to sort 
def SortPolishString(table,sort_id):

	for i,word in enumerate(table):
		table[i] = list(table[i])
		table[i][sort_id] = codeString(word[sort_id])
	
	table.sort(key = itemgetter(sort_id))

	for i,word in enumerate(table):
		# print(len(word[sort_id]))
		table[i][sort_id] =  decodeString(word[sort_id])
		# print(len(table[i][sort_id])/3)
	return table;




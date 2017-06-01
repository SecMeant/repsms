import sqlite3
from operator import itemgetter

#Taking cursor to database and query that will be runned
#Returns dictionary that have indexes named like columns from database
#that points to data from database
def sqlDict(cursor, query):
	result = cursor.execute(query)
	i = len(result.description)
	j = 0
	sDict = {}
	data = []
	rows = result.fetchall()

	#Making tables. Each table contains table of each column from database
	while(i > 0):
		data.append([])
		for each in rows:
			data[j].append(each[j])
		i = i-1
		j = j+1

	#Making indexes to dictionary
	index = []
	for each in result.description:
		index.append(each[0])

	#Combining indexes with data in dictionary
	j=0
	for each in index:
		sDict.update({ each:data[j] })
		j = j+1

	return sDict

#This funtions takes sqlDict and returns normal table of tables
#This is usefull when u need to call sorted on sqlDict
#entries is number of most elements that key points to
def sqlDict_toSortableTable(instance_sqlDict,entries):
	stab = []
	xtab = []
	i = 0
	while(i<entries):
		for each in instance_sqlDict:
			try:
				stab.append(instance_sqlDict[each][i])
			except:
				stab.append(None)
		xtab.append(stab)
		stab = []
		i = i+1

	return xtab

def sqlDict_sort(instance_sqlDict,entries,itemget):
	tab = sqlDict_toSortableTable(instance_sqlDict, entries)
	tab = sorted(tab,key=lambda l:l[itemget],reverse=True) # Sortowane po punktach
	i = 0
	j = 0

	for each in instance_sqlDict:
		instance_sqlDict[each] = []


	while(i < entries):
		for each in instance_sqlDict:
			instance_sqlDict[each].append(tab[i][j])
			j+=1
		j=0
		i+=1

	return instance_sqlDict


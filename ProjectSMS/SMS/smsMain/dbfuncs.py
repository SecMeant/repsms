import sqlite3

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
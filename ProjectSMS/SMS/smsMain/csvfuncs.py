def searchcsv(phrase,file):
	file.seek(0)
	line = file.readline().decode('utf-8')
	fline = line.split(";")
	i=0
	for word in fline:
		if(word == phrase):
			return i
		i+=1

	return None

def fixnames(table):
	strtable = ''
	i=0
	while(i<len(table)):
		strtable = table[i]
		strtable = strtable.replace(" ", "_")
		table[i] = strtable
		i+=1

	return table

def generateQuery(tablename,columns,numOfValues,prefix):
	if(prefix == "INSERT INTO"):
			query = "INSERT INTO " + tablename + " ("
			i=0
			while(i<len(columns)-1):
				query += columns[i] + ","
				i+=1
			query += columns[i] + ") VALUES ("
			j=0
			while(j<numOfValues-1):
				query += "?,"
				j+=1
			query += "?)"
	return query

def generateValue(values,offset):
	query = ""
	i=0
	while(i<len(offset)-1):
		query += values[offset[i]] + ","
		i+=1
	query += values[offset[i]]
	return query.split(",")

def fixWanted(wanted,offset):
	i = 0
	while(i<len(offset)):
		if(offset[i] == ''):
			del wanted[i]
			del offset[i]
			i-=1
		i+=1
	return wanted


def importcsv(colms,offset,file,cursor):
	fixnames(colms) # Naprawiam niektore nazwy bo sqlite nie lubi ze spacjami
	colms = fixWanted(colms,offset) # Wyrzucam z wanted table kolumny ktorych nie znalazlem poniewaz nie beda one uzyte w kwerendzie
	print("colms:  ",colms)
	print("offset:  ",offset)
	cursor.execute("CREATE TABLE IF NOT EXISTS uczniowie(id INTEGER PRIMARY KEY AUTOINCREMENT)")
	for word in colms:
		try:
			cursor.execute("ALTER TABLE uczniowie ADD " + word + " text")
		except :
			print("Column " + word + " exists !")
	
	query = generateQuery("uczniowie",colms,len(colms),"INSERT INTO")
	line = file.readline().decode('utf-8')
	fline = line.split(";")
	
	while(line):
		string = generateValue(fline,offset)

		#For loop changes all fields from 'null' to 0
		#nulls causes some problems in fill / opt functions
		for i,s in enumerate(string):
			if(s == 'null'):
				string[i] = 0
				
		cursor.execute(query ,string)
		line = file.readline().decode('utf-8')
		fline = line.split(";")


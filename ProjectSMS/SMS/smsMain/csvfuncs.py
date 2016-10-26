def searchcsv(phrase,file):
				# file = open(filename,"r+",encoding="utf8")
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

def importcsv(colms,offset,file,cursor):
	# file = open(filename,"r+",encoding="utf8")
	fixnames(colms)
	cursor.execute("CREATE TABLE IF NOT EXISTS uczniowie(id INTEGER PRIMARY KEY AUTOINCREMENT)")
	for word in colms:
		try:
			cursor.execute("ALTER TABLE uczniowie ADD " + word + " text")
		except :
			print("Column " + word + " exists !")



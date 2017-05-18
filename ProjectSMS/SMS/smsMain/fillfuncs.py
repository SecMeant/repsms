from operator import itemgetter
import math

# ARGS:
# c is currsor for database
# conn is handle for connection to database
# klasa is row from database for class that algorithm will be runned
# uczniowie are rows from database that contains all of the students that will be part of a class
# user is name of user who is running this function, name of the table will contain users name
# odp is table that was returned from optimaizing functions, it contains size of optimized classes
def fillclasses(c,conn,klasa,uczniowie,user,odp):
	c.execute("SELECT * FROM algorytmy WHERE id="+str(klasa[0][3]))
	algo = c.fetchall()

	points = 0
	buff = 0
	while(buff < len(uczniowie)):
		if(uczniowie[buff][13]):
			points = int(uczniowie[buff][13]) * algo[0][2]
		if(uczniowie[buff][14]):
			points += int(uczniowie[buff][14]) * algo[0][3]
		if(uczniowie[buff][15]):
			points += int(uczniowie[buff][15]) * algo[0][4]
		if(uczniowie[buff][16]):
			points += int(uczniowie[buff][16]) * algo[0][5]

		uczniowie[buff].append(points)
		buff += 1

	#Im not sure if this move is OK...
	#However it works, so at least now Ill leave it
	#I did this cuz sorted() throwed some errors like it cant
	#compare Nonetype and str etc
	#I dont even remember why I need to call sorted()
	##################################
	#			DIRTY TRICKS		 #
	for i,s in enumerate(uczniowie):
			for j,v in enumerate(s):
				if(v == None):
					s[j] = '0'	
	##################################

	uczniowie = sorted(uczniowie,key=itemgetter(18),reverse=True)

	letter = klasa[0][4]

	inc = 0
	inc2 = 0
	j = 0

	if(odp==0):
		perclass = math.ceil(len(uczniowie)/klasa[0][2])

		while(inc < perclass):
			if(ord(letter)>90):
				print("UWAGA INDEX 'Z' PRZY KLASIE. IM KILLING THE ALGORITHM !")
				return 1
			nazwaNowejKlasy = user.username+klasa[0][0]+letter
			query = "CREATE TABLE IF NOT EXISTS '"+nazwaNowejKlasy+"' (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, Imię text, Nazwisko text , Kod_pocztowy text, Miejscowość text, Ulica text, Nr_budynku text, Nr_mieszkania text, Kod_pocztowy2 text, Miejscowość2 text, Ulica2 text, Nr_budynku2 text, Nr_mieszkania2 text, polski text, angielski text, niemiecki text, francuski text, wloski text, hiszpanski text,rosyjski text, matematyka text, fizyka text, informatyka text, historia text, biologia text, chemia text, geografia text, wos text, zajęcia_techniczne text, zajęcia_artstyczne text, edukacja_dla_bezpieczeństwa text, plastyka text, muzyka text, wf text, zachowanie text, klasa text,punkty text)"
			c.execute(query)
			conn.commit()
			while(inc2 < klasa[0][2] and j<len(uczniowie)):
				query = "INSERT INTO "+nazwaNowejKlasy+" ('Imię','Nazwisko','Kod_pocztowy','Miejscowość','Ulica','Nr_budynku','Nr_mieszkania','Kod_pocztowy2','Miejscowość2','Ulica2','Nr_budynku2','Nr_mieszkania2','polski','angielski','niemiecki','francuski','wloski','hiszpanski','rosyjski','matematyka','fizyka','informatyka','historia','biologia','chemia','geografia','wos','zajęcia_techniczne','zajęcia_artstyczne','edukacja_dla_bezpieczeństwa','plastyka','muzyka','wf','zachowanie','klasa','punkty') "
				query += "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
				c.execute(query,uczniowie[j][1:])
				c.execute("UPDATE uczniowie SET klasa=? WHERE id=?",(nazwaNowejKlasy,uczniowie[j][0]))
				conn.commit()
				j += 1
				inc2 += 1
			inc2 = 0
			inc += 1
			letter = ord(letter)
			letter += 1
			letter = chr(letter)

		c.execute("UPDATE klasy SET litera=\'"+letter+"\' WHERE id="+str(klasa[0][5]))
		conn.commit()
		conn.close()
	else:
		n = 0
		while(inc < len(odp[0])):
			if(ord(letter)>90):
				print("UWAGA INDEX 'Z' PRZY KLASIE. IM KILLING THE ALGORITHM !")
				return 1
			nazwaNowejKlasy = user.username+klasa[0][0]+letter
			query = "CREATE TABLE IF NOT EXISTS '"+nazwaNowejKlasy+"' (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, Imię text, Nazwisko text , Kod_pocztowy text, Miejscowość text, Ulica text, Nr_budynku text, Nr_mieszkania text, Kod_pocztowy2 text, Miejscowość2 text, Ulica2 text, Nr_budynku2 text, Nr_mieszkania2 text, polski text, angielski text, niemiecki text, francuski text, wloski text, hiszpanski text,rosyjski text, matematyka text, fizyka text, informatyka text, historia text, biologia text, chemia text, geografia text, wos text, zajęcia_techniczne text, zajęcia_artstyczne text, edukacja_dla_bezpieczeństwa text, plastyka text, muzyka text, wf text, zachowanie text, klasa text,punkty text)"
			c.execute(query)
			conn.commit()
			while(inc2 < odp[0][n] and j<len(uczniowie)):
				query = "INSERT INTO "+nazwaNowejKlasy+" ('Imię','Nazwisko','Kod_pocztowy','Miejscowość','Ulica','Nr_budynku','Nr_mieszkania','Kod_pocztowy2','Miejscowość2','Ulica2','Nr_budynku2','Nr_mieszkania2','polski','angielski','niemiecki','francuski','wloski','hiszpanski','rosyjski','matematyka','fizyka','informatyka','historia','biologia','chemia','geografia','wos','zajęcia_techniczne','zajęcia_artstyczne','edukacja_dla_bezpieczeństwa','plastyka','muzyka','wf','zachowanie','klasa','punkty') "
				query += "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
				c.execute(query,uczniowie[j][1:])
				c.execute("UPDATE uczniowie SET klasa=? WHERE id=?",(nazwaNowejKlasy,uczniowie[j][0]))
				conn.commit()
				j += 1
				inc2 += 1
			n += 1
			inc2 = 0
			inc += 1
			letter = ord(letter)
			letter += 1
			letter = chr(letter)

		c.execute("UPDATE klasy SET litera=\'"+letter+"\' WHERE id="+str(klasa[0][5]))
		conn.commit()
		conn.close()
	return 0
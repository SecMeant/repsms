from math import floor
def dejnumer(ileuczniow,max_i=36):
	klasy=0
	maxvar=max_i
	temp=ileuczniow

	klasy=0
	while(temp>0):
		temp-=maxvar
		klasy+=1
	
	odpowiedz = [0] * 3
	if(temp == 0):
		odpowiedz[0]=maxvar
		odpowiedz[1]=temp
		odpowiedz[2]=klasy
		return odpowiedz
	
	if(temp<0):
		temp+=maxvar

	while(temp<maxvar):
		temp+=klasy-1
		maxvar-=1
	
	odpowiedz[0]=maxvar
	odpowiedz[1]=temp
	odpowiedz[2]=klasy
	return odpowiedz		

def optymalizuj(tab,max_i=36):
	print("tab:")
	print(tab)
	if(tab[1]!=0):
		i=0
		tabklas = [0] * tab[2]
		while(i<tab[2]-1):
			tabklas[i]=tab[0]
			i+=1

		tabklas[tab[2]-1]=tab[1]
		
		j=0
		while(tabklas[0]-tab[1]>2):
			tabklas[j]-=1
			tab[1]+=1
			if(j==tab[2]-1):
				j=0
			j+=1

		if(tab[1]>max_i):
			reszta=tab[1]-max_i
			tab[1]-=reszta
				
			i=0
			while(reszta>0):
				tabklas[i]+=1
				reszta-=1
				i+=1

		tabklas[tab[2]-1]=tab[1]

	else:
		g=0
		while(g<tab[2]):
			tabklas[g]=tab[0]
			g+=1
	return tabklas

def rest(odp):
	sizeof = len(odp);
	minvar = odp[0];
	toadd = 0;
	
	i=0
	while(i<sizeof):
		if(odp[i] < minvar):
			minvar = odp[i]
		i+=1

	i=0
	while(i<sizeof):
		if(odp[i] > minvar):
			toadd += odp[i] - minvar;
			odp[i] = minvar
		i+=1

	i=0
	while(toadd>0):
		odp[i]+=1
		toadd-=1
		if(i == sizeof-1):
			i=0
		i+=1
	
	return odp

def simpleodp(ileuczniow,max_i=36):
	odpowiedz = []
	odpowiedz.append(( ileuczniow % max_i )) # reszta
	odpowiedz.append(max_i) # rozmiar klasy
	odpowiedz.append(0)
	if(odpowiedz[0] > 0):
		odpowiedz[2] = floor( ileuczniow / max_i ) +1 # ile klas
	else:
		odpowiedz[2] = round( ileuczniow / max_i ) # ile klas
	i = 0;
	
	while(i < odpowiedz[2] - 1):
		odp[i] = max_i; 
		i+=1;
	
	odp[i] = odpowiedz[0];

	return odp;

def simpleodpowiedzi(ileuczniow,max_i=36):
	odpowiedz = []
	odpowiedz.append( ileuczniow % max_i ) # reszta
	odpowiedz.append( max_i ) # rozmiar klasy
	if(odpowiedz[0] > 0):
		odpowiedz[2] = floor( ileuczniow / max_i ) +1 # ile klas
	else:
		odpowiedz[2] = round( ileuczniow / max_i ) # ile klas
	
	return odpowiedz
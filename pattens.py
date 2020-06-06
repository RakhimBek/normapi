# city, house, favella

bad = pd.read_csv('bad.csv', sep=';')
bad['city'] = bad['address'].str.extract('(г\.\ ?[а-яА-Я]+)') # город
bad['house'] = bad['address'].str.extract('(д\.\ ?[0-9]+[а-яА-Я]?|дом\ ?[0-9]+[а-яА-Я]?)') # дом
bad['favella'] = bad['address'].str.extract('(д\.\ ?[а-яА-Я-]+)') # деревня


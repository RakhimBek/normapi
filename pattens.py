# city, house

bad = pd.read_csv('bad.csv', sep=';')
bad['city'] = bad['address'].str.extract('(г\.\ ?[а-яА-Я]+)')
bad['house'] = bad['address'].str.extract('(д\.\ ?[0-9]+[а-яА-Я]?|дом\ ?[0-9]+[а-яА-Я]?)')

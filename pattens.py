# city, house, favella

bad['address'] = bad['address'].str.replace('I', '1')
bad['address'] = bad['address'].str.replace('II', '2')
bad['address'] = bad['address'].str.replace('III', '3')
bad['address'] = bad['address'].str.replace('IV', '4')
bad['address'] = bad['address'].str.replace('V', '5')
bad['address'] = bad['address'].str.replace('VI', '6')
bad['address'] = bad['address'].str.replace('VII', '7')
bad['address'] = bad['address'].str.replace('VIII', '8')
bad['address'] = bad['address'].str.replace('IX', '9')
bad['address'] = bad['address'].str.replace('X', '10')
bad['address'] = bad['address'].str.replace('XI', '11')
bad['address'] = bad['address'].str.replace('XII', '12')
bad['address'] = bad['address'].str.replace('XIII', '13')

bad['city'] = bad['address'].str.extract('(г\.?\ ?[А-Я][а-яА-Я-]+)')
bad['city'] = bad['city'].replace(np.nan, '', regex=True)
bad['address'] = bad['address'].str.replace('(г\.?\ ?[а-яА-Я-]+)', '')

bad['hous'] = bad['address'].str.extract('(д\.\ ?[0-9]+[а-яА-Я]?|дом\ ?[0-9]+[а-яА-Я]?)')
bad['hous'] = bad['hous'].replace(np.nan, '', regex=True)
bad['address'] = bad['address'].str.replace('(д\.\ ?[0-9]+[а-яА-Я]?|дом\ ?[0-9]+[а-яА-Я]?)', '')

bad['favella'] = bad['address'].str.extract('(д\.\ ?[а-яА-Я-]+)')
bad['favella'] = bad['favella'].replace(np.nan, '', regex=True)
bad['address'] = bad['address'].str.replace('(д\.\ ?[а-яА-Я-]+)', '')

bad['lane'] = bad['address'].str.extract('(пер\.?[еулок]*\ ?[^ ,]+)')
bad['lane'] = bad['lane'].replace(np.nan, '', regex=True)
bad['address'] = bad['address'].str.replace('(пер\.?[еулок]*\ ?[^ ,]+)', '')

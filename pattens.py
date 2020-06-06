import pandas as pd
import numpy as np

# city, house, favella

street = r'(ул\.?\s\w+(\s\w+)?|улица\s\w+(\s\w+)?|\w+(\s\w+)?\sулица|\w+(\s\w+)?\sул\.?)'
area = r'(обл\.?\s\w+|область\s\w+|\w+\sобласть|\w+\sобл\.?)'
bad = pd.read_csv('bad.csv', sep=';')
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

bad['city'] = bad['address'].str.extract(r'(г\.?\ ?[А-Я][а-яА-Я-]+)')
bad['city'] = bad['city'].replace(np.nan, '', regex=True)
bad['address'] = bad['address'].str.replace(r'(г\.?\ ?[а-яА-Я-]+)', '')

bad['hous'] = bad['address'].str.extract(r'(д\.\ ?[0-9]+[а-яА-Я]?|дом\ ?[0-9]+[а-яА-Я]?)')
bad['hous'] = bad['hous'].replace(np.nan, '', regex=True)
bad['address'] = bad['address'].str.replace(r'(д\.\ ?[0-9]+[а-яА-Я]?|дом\ ?[0-9]+[а-яА-Я]?)', '')

bad['favella'] = bad['address'].str.extract(r'(д\.\ ?[а-яА-Я-]+)')
bad['favella'] = bad['favella'].replace(np.nan, '', regex=True)
bad['address'] = bad['address'].str.replace(r'(д\.\ ?[а-яА-Я-]+)', '')

bad['lane'] = bad['address'].str.extract(r'(пер\.?[еулок]*\ ?[^ ,]+)')
bad['lane'] = bad['lane'].replace(np.nan, '', regex=True)
bad['address'] = bad['address'].str.replace(r'(пер\.?[еулок]*\ ?[^ ,]+)', '')

bad['street'] = bad['address'].str.extract(street)
bad['street'] = bad['street'].replace(np.nan, '', regex=True)
bad['address'] = bad['address'].str.replace(street, '')

bad['area'] = bad['address'].str.extract(area)
bad['area'] = bad['area'].replace(np.nan, '', regex=True)
bad['address'] = bad['address'].str.replace(area, '')

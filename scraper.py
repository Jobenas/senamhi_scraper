import requests
import pandas as pd
from bs4 import BeautifulSoup

html = requests.get('http://www.senamhi.gob.pe/peruclima/maps/map_data_ca.php').content

data_array = html.split('<head')
head_array =  data_array[1].split('<!--')[0].split('\r\n')

useful_data = head_array[5].split('<script')[1].split('</script')[0].split('type="text/javascript">')[1].split('locations = ')[1].split('],[')
useful_data[0] = useful_data[0].split('[[')[1]
for i in useful_data:
	if "SAN BORJA" in i:
		soup = BeautifulSoup(i, 'lxml')  # Parse the HTML as a string
		html_table = soup.find_all('table')  # Grab the first table
		# print html_table

		tables = []
		for i in html_table:
			soup = BeautifulSoup(str(i), 'lxml')  # Parse the HTML as a string

			table = soup.find_all('table')[0]  # Grab the first table

			new_table = []

			row_marker = 0
			for row in table.find_all('tr'):
				# print "new row"
				row_element = []
				column_marker = 0
				columns = row.find_all('td')
				for column in columns:
					# print column.get_text()
					column_text = column.get_text()
					row_element.append(column_text)
					column_marker += 1
				if len(row_element) > 0:
					new_table.append(row_element)
				row_marker += 1

			if len(new_table) > 0:
				tables.append(new_table)

		for j in tables:
			print j
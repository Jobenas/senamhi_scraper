import requests
import pandas as pd
from bs4 import BeautifulSoup
import pyowm
import urllib
import urllib2
import json

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

		last_data = tables[1][0]
		date = last_data[0]
		date = date.split('/')
		date = date[2] + "-" + date[1] + "-" + date[0][1:]

		timestamp = date + " " + last_data[1][1:]
		no2 = last_data[2]
		so2 = 0.0
		pm10 = last_data[4]
		pm25 = last_data[5]
		o3 = last_data[6]
		co = last_data[7]

owm = pyowm.OWM('6ec107ebbe662eae76512e5608ac1344')
observation = owm.weather_at_place('Lima,pe')
w = observation.get_weather()
temperature = w.get_temperature('celsius')['temp']
humidity = w.get_humidity()

payload = {}

payload['temp'] = temperature
payload['hum'] = humidity
payload['sensor_id'] = 1
payload['timestamp'] = timestamp
payload['co'] = co
payload['o3'] = o3
payload['no2'] = no2
payload['pm10'] = pm10
payload['pm25'] = pm25
payload['so2'] = so2
payload['co2'] = 0.0
payload['pm1'] = 0.0
payload['uv'] = 0.0
payload['lum'] = 0.0
payload['sonido'] = 0.0
payload['username'] = "jobenas"
payload['pwd'] = "passw0rd"

url = "https://limaio.jobenas.com/limaio/api/v1.0/registerReading"

request = urllib2.Request(url)
request.add_header('Content-Type', 'application/json')

print payload

response = urllib2.urlopen(request, json.dumps(payload))
html = response.read()

print html
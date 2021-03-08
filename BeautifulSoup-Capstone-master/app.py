from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr', attrs={'class':''})
temp = [] #initiating a tuple

for i in range(1, len(tr)):
	row = table.find_all('tr', attrs = {'class':''})[i]
	
	date = row.find_all('td')[0].text
	date = date.strip()
	day = row.find_all('td')[1].text
	day = day.strip()
	value = row.find_all('td')[2].text
	value = value.strip()
	
	temp.append((date, day, value))
#insert the scrapping process here

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('date', 'day', 'value'))
df['value'] = df['value'].replace('IDR',"",regex=True).replace(',',"",regex=True)
df['value'] = df['value'].astype('float64')
df['date'] = df['date'].astype('datetime64')

#insert data wrangling here

df.set_index('date', inplace=True)
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {round(df["value"].mean(),2)}'

	# generate plot
	ax = df.plot(figsize = (15,6))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)

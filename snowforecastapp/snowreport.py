#Valdezcaray Ski Resort Snowforecast and Snow Report
import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

#Update actual weather (each 10 minutes)
@st.cache_data(ttl=600)
def updateSnowReport():
	try:
		response = requests.get("https://www.valdezcaray.es/parte-de-nieve/")
	except requests.exceptions.ConnectionError:
		print("Connection refused")
		return None

	soup = BeautifulSoup(response.content, "html.parser")
	tiempo = soup.find('div', class_='tiempo')
	actual = tiempo.text.strip()
	actual_icon = tiempo.find('img')['src']
	pistas = soup.find('div', class_='pistas')
	slopes = pistas.text.strip()
	slopes_icon = pistas.find('img')['src']
	remontes = soup.find('div', class_='remontes')
	lifts = remontes.text.strip()
	lifts_icon = remontes.find('img')['src']
	return actual, actual_icon, slopes, slopes_icon, lifts, lifts_icon

#Update forecast (each 1 hour)
@st.cache_data(ttl=3600)
def updateForecast():
	forecast = []
	try:
		response = requests.get("https://www.meteoexploration.com/en/forecasts/Valdezcaray/")
	except requests.exceptions.ConnectionError:
		print("Connection refused")
		return forecast

	soup = BeautifulSoup(response.content, 'html.parser')

	dates = soup.find_all(class_='date')
	temps_min = soup.find_all(class_='Tmin')
	temps_max =soup.find_all(class_='Tmax')
	snows =soup.find_all(class_='pcpsnow')

	icons = soup.find_all(class_="iconW")

	for i in range(7):
		date = dates[i].text.strip()
		tmin = temps_min[i].text.strip()
		tmax = temps_max[i].text.strip()
		snow = snows[i].text.strip()
		icon = "https://www.meteoexploration.com/" + icons[i].find('img')['src']
		forecast.append({"date": date, "tmin": tmin, "tmax": tmax, "snow": snow, "icon": icon})
	return forecast

#Update webcam images (each 5 minutes)
@st.cache_data(ttl=100)
def updateWebCams():
	images = []
	timestamp = int(time.time())
	images.append(f"https://www.valdezcaray.es/webcam/Parking/parking.jpg?intmp=={timestamp}")
	images.append(f"https://www.valdezcaray.es/webcam/Principal/principal.jpg?intmp=={timestamp}")
	images.append(f"https://www.valdezcaray.es/webcam/Principal/principal.jpg?intmp=={timestamp}")
	images.append(f"https://www.valdezcaray.es/webcam/Colocobia/colocobia.jpg?intmp=={timestamp}")
	return images

st.set_page_config(page_title="Valdezcaray", page_icon=":snowflake:")
st.title("Valdezcaray Ski Resort")
actual_placeholder = st.empty()
forecast_placeholder = st.empty()
webcams_placeholder = st.empty()

while True:

	#Update iformation
	snow_report = updateSnowReport()
	forecast = updateForecast()
	webcams = updateWebCams()

	actual_placeholder.empty()
	forecast_placeholder.empty()
	webcams_placeholder.empty()

	#Show Snow Report
	with actual_placeholder.container():
		st.header("Snow Report")
		if snow_report is not None:
			col1,col2,col3 = st.columns(3)
			with col1:
				st.write("Current Weather")
				st.image(snow_report[1], width = 50,  output_format = "JPG")
				st.write(f":orange[{snow_report[0].split()[1]}]")
			with col2:
				st.write("Slopes")
				st.image(snow_report[3], width = 50, output_format = "JPG")
				st.write(f":orange[{snow_report[2].split()[1]}]")
			with col3:
				st.write("Lifts")
				st.image(snow_report[5], width = 50, output_format = "JPG")
				st.write(f":orange[{snow_report[4].split()[1]}]")
		else:
			st.write("Connection refused.")
	#Show snow forecast
	with forecast_placeholder.container():
		st.header("Snow forecast")
		if len(forecast) >cm 7:
			columns = st.columns(7)
			with columns[0]:
				st.write("Day:")
				st.write("Min:")
				st.write("Max:")
				st.write("Snow:")
				st.write("")
			for i in range(1,7):
				with columns[i]:
					st.write(forecast[i]["date"])
					st.write(forecast[i]["tmin"])
					st.write(forecast[i]["tmax"])
					st.write(forecast[i]["snow"])
					st.image(forecast[i]["icon"])
		else:
			st.write("Connection refused.")

	#Show webcams
	with webcams_placeholder.container():
		st.header("Webcams")
		col1, col2 = st.columns(2)

		for i in range(0,len(webcams),2):
			col1, col2 = st.columns(2)

			with col1:
				st.image(webcams[i],use_column_width=True)

			with col2:
				st.image(webcams[i+1],use_column_width=True)
	#Wait for update It should be 5 minutes as the webcams updates.
	time.sleep(300)

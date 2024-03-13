import streamlit as st
import requests
import time

#Request data and load into a json.
def requestData():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    data = response.json()
    return data

# Función para obtener el avatar utilizando el id como seed
def getIdenticon(id):
    avatar = f"https://api.dicebear.com/7.x/notionists/svg?seed={id}"
    return avatar

# Función para mostrar los datos en la interfaz de Streamlit
def updateData(data):
    avatar = getIdenticon(data['id'])
    st.image(avatar, width=100)
    st.write("ID:", data['id'])
    st.write("UserId:", data['userId'])
    st.write("Title:", data['title'])
    st.write("Body:", data['body'])

# Configurar la aplicación Streamlit
st.title("Week 5 - Test")

#Get data
file = requestData()

i = 0
placeholder = st.empty()

#Iterate data each 5 seconds
while True:
    placeholder.empty()
    with placeholder.container():
        updateData(file[i])
    i += 1
    if i > 10:
        i = 0
    time.sleep(10)


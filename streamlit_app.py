# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
	)
import streamlit as st 
name_on_order = st.text_input("Name on the Smoothie")
st.write("The name on the Smoothie is ", name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
	'Choose up to 5 ingredients:'
	, my_dataframe
	, max_selections=5
	)
	
if ingredients_list:  
	ingredients_string= ' '
	for fruit_choosen in ingredients_list:
		ingredients_string += fruit_choosen + ' '
		st.subheader(fruit_choosen + ' Nutrition Information')
	smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choosen)
	sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choosen)
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

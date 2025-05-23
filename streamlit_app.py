# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
)

name_on_order = st.text_input("Name on the Smoothie")
st.write("The name on the Smoothie is ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))

#Convert the Snowpark Dataframe to Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
	'Choose up to 5 ingredients:'
	, my_dataframe
    , max_selections=5
	)

if ingredients_list:
   ingredients_string = ''
   for fruit_choosen in ingredients_list:
  	ingredients_string += fruit_choosen + ' '
	 
    	search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
    	#st.write('The search value for ', fruit_choosen,' is ', search_on, '.') 
	 
    	st.subheader(fruit_choosen + ' Nutrition Information')
    	smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
    	sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
	 
my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
	values ('""" + ingredients_string + """','""" + name_on_order +"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

if time_to_insert:
    	session.sql(my_insert_stmt).collect()
    	st.success('Your Smoothie is ordered!', icon="✅")
	
# New section to display smoothiefroot nutrition information 

#st.text(smoothiefroot_response.json())

# # Import python packages
# import streamlit as st
# from snowflake.snowpark.context import get_active_session
# from snowflake.snowpark.functions import col

# # Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
# st.write(
#     """Choose the fruits you want in your custom smoothie! 
#     """
# )


# name_on_order = st.text_input("Name on Smoohtie:")
# st.write("The name on your smoothie will be:", name_on_order)


# # option = st.selectbox(
# #     "What is your favourite fruit?",
# #     ("Banana", "Strawberries", "Peaches"))

# # st.write("Your favourite fruit is:", option)

# session = get_active_session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# # st.dataframe(data=my_dataframe, use_container_width=True)

# ingredients_list = st.multiselect('Choose upto 5 ingredients:',my_dataframe)

# # st.write(ingredients_list)
# # st.text(ingredients_list)

# if ingredients_list:
#     # st.write(ingredients_list)
#     # st.text(ingredients_list)
    
#     ingredients_string = ''
    
#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '

#     # st.write(ingredients_string)

#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
#             values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#     st.write(my_insert_stmt)
#     # st.stop()

#     time_to_insert = st.button('Submit Order')
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")
     
    

    

import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Set up Streamlit app title and initial instructions
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# User input for smoothie name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Get active Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()

# Retrieve fruit names from Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
fruit_options = [row[0] for row in my_dataframe]

# Multiselect widget for choosing ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_options, [], key='ingredients', max_selections = 5)

# Display selected ingredients
if ingredients_list:
    # st.write("Selected ingredients:")
    # for ingredient in ingredients_list:
    #     # st.write("- " + ingredient)

    # Button to submit smoothie order
    time_to_insert = st.button('Submit Order')
    if time_to_insert and name_on_order:
        ingredients_string = ', '.join(ingredients_list)

        # SQL INSERT INTO statement to insert order into Snowflake table
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered, ' + name_on_order, icon="✅")
        except Exception as e:
            st.error(f'Error submitting order: {str(e)}')

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display title and description
st.title("Jsk Order Management")
st.markdown("Enter details below")

# Establshing a google sheet
conn = st.connection("gsheets", type = GSheetsConnection)
#conn = st.experimental_connection("gsheets", type=GSheetsConnection, file_id="1O-nhrrOukKpQoE3-Kdk-bjpk2GENwcTe9K5EDXqtnpw")


# fetching existing data

existing_data = conn.read(worksheet = "Order", usecols = list(range(6)), ttl = 5)
existing_data = existing_data.dropna(how = "all")

#st.dataframe(existing_data)

#list of details needed

Details = ["Date","Time","Location","Amount", "Commision", "Contact No."]
Time = ["HalfDay","FullDay"]

# The new data
with st.form(key="Order"):
    date = st.date_input(label = "Today Date")
    time = st.selectbox(label = "Select the time", options= Time)
    location = st.text_input(label = "Location")
    amount = st.text_input(label = "Amount")
    commision = st.text_input(label = "Commision")
    contact  = st.text_input(label="Phone Num")

    #mark mandatory fields

    st.markdown("**required*")

    submit_button = st.form_submit_button(label = "Submit")


    if submit_button:
        if not date or not time or not location or not amount:
            st.warning("Please fill up the mandatory fields")
            st.stop()
        else:
            #create new row
            order_data = pd.DataFrame([
                {
                "Date": date.strftime("%d-%m-%Y"),
                "Time": time,
                "Location": location,
                "Commision": commision,
                "Amount": amount,
                "Contact No.": contact

                }
                
            ])

            #add the new data into sheet

        update_df = pd.concat([existing_data, order_data], ignore_index = True)

        #update the google sheet

        conn.update(worksheet = "Order", data = update_df)

        st.success("Thank You")

#("gsheets", type = GSheetsConnection())

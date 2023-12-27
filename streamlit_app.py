import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display title and description
st.title("Jsk Order Management")
st.markdown("Enter details below")

# Establishing a google sheet connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetching existing data
existing_data = conn.read(worksheet="Order", usecols=list(range(7)), ttl=5)
existing_data = existing_data.dropna(how="all")

# List of details needed
Details = ["Mr:", "Date", "Time", "Location", "Amount", "Commision", "Contact No."]
Time = ["HalfDay", "FullDay"]
Name = ["Ravi", "Sumin"]

# The new data
with st.form(key="Order"):
    name = st.selectbox(label="Name:", options=Name)
    date = st.date_input(label="Today Date")
    time = st.selectbox(label="Select the time", options=Time)
    location = st.text_input(label="Location")
    amount = st.text_input(label="Amount")
    commision = st.text_input(label="Commision")
    contact = st.text_input(label="Phone Num")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if not all([date, time, location, amount]):
            st.warning("Please fill up all mandatory fields")
            st.stop()
        else:
            # Create new row
            order_data = pd.DataFrame([
                {
                    "Name": name,
                    "Date": date.strftime("%d-%m-%Y"),
                    "Time": time,
                    "Location": location,
                    "Commision": commision,
                    "Amount": amount,
                    "Contact No.": contact
                }
            ])

            # Add the new data into the sheet
            update_df = pd.concat([existing_data, order_data], ignore_index=True)

            # Update the google sheet
            conn.update(worksheet="Order", data=update_df)

            st.success("Thank You")

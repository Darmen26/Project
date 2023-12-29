import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display title and description
st.title("J Star Keeranaa Order")
st.markdown("Masukkan Butiran dibawah:")

# Establishing a google sheet connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetching existing data
existing_data = conn.read(worksheet="Order", usecols=list(range(8)), ttl=5)
existing_data = existing_data.dropna(how="all")

# List of details needed
Details = ["Name:", "Tarikh", "Waktu", "Lokasi","OT", "Jumlah", "Komisyen", "No.Telephone"]
Time = ["Setengah Hari", "Satu Hari"]
Name = ["Ravi", "Sumin"]
Payment = ["Cash","Bank","X"]


# The new data
with st.form(key="Order"):
    name = st.radio(label="Name:", options=Name)
    date = st.date_input(label="Tarikh:")
    company = st.text_input(label="Name Syarikat:")
    contact = st.text_input(label="No.Telephone:")
    bill = st.text_input(label="Nombor Do:")
    location = st.text_input(label="Lokasi:")
    time = st.radio(label="Waktu:", options=Time)
    ot = st.text_input(label = "OT:")
    amount = st.text_input(label="Jumlah:")
    commision = st.text_input(label="Komisyen:")
    payment =  st.radio(label="Payment:", options=Payment)
    

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if not all([date, time, location, amount,company,payment]):
            st.warning("Sila isi semua perkara")
            st.stop()
        else:
            # Create new row
            order_data = pd.DataFrame([
                {
                    "Name": name,
                    "Date": date.strftime("%d-%m-%Y"),
                    "Company": company,
                    "Contact": contact,
                    "Bill":bill,
                    "Location": location,
                    "Time": time,
                    "OT":ot,
                    "Commision": commision,
                    "Jumlah": amount,
                    "Payment": payment
                }
            ])

            # Add the new data into the sheet
            update_df = pd.concat([existing_data, order_data], ignore_index=True)

            # Update the google sheet
            conn.update(worksheet="Order", data=update_df)

            st.success("Thank You")

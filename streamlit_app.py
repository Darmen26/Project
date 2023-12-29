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

# The new data
with st.form(key="Order"):
    name = st.radio(label="Name:", options=Name)
    date = st.date_input(label="Tarikh")
    time = st.selectbox(label="Waktu", options=Time)
    location = st.text_input(label="Lokasi")
    ot = st.text_input(label = "OT")
    amount = st.text_input(label="Jumlah")
    commision = st.text_input(label="Komisyen")
    contact = st.text_input(label="No.Telephone")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if not all([date, time, location, amount]):
            st.warning("Sila isi semua perkara")
            st.stop()
        else:
            # Create new row
            order_data = pd.DataFrame([
                {
                    "Name": name,
                    "Tarikh": date.strftime("%d-%m-%Y"),
                    "Waktu": time,
                    "Lokasi": location,
                    "OT":ot,
                    "Komisyen": commision,
                    "Jumlah": amount,
                    "No.Telephone": contact
                }
            ])

            # Add the new data into the sheet
            update_df = pd.concat([existing_data, order_data], ignore_index=True)

            # Update the google sheet
            conn.update(worksheet="Order", data=update_df)

            st.success("Thank You")

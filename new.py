import streamlit as st
import pandas as pd
import yagmail

# Configuration
SENDER_EMAIL = "eclipse.203504@gmail.com"
RECEIVER_EMAIL = "rmmani80@gmail.com"
EMAIL_PASSWORD = "iihupeibylcdnjpx"  # Replace with your newly generated app password.

# Function to save data to Excel
def save_to_excel(data, filename="data.xlsx"):
    try:
        # Load existing data or create a new one if the file doesn't exist
        df = pd.read_excel(filename) if filename else pd.DataFrame(columns=["Name", "Location", "Object Type"])
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
        df.to_excel(filename, index=False)
    except FileNotFoundError:
        pd.DataFrame(data).to_excel(filename, index=False)

# Function to read data from Excel
def read_from_excel(filename="data.xlsx"):
    try:
        return pd.read_excel(filename)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Location", "Object Type"])

# Function to send email
def send_email(data, recipient_email):
    # Format the message
    message = "\n\n".join(
        f"Name: {row['Name']}\nLocation: {row['Location']}\nObject Purchased: {row['Object Type']}"
        for _, row in data.iterrows()
    )
    
    # Setup email
    try:
        yag = yagmail.SMTP(SENDER_EMAIL, EMAIL_PASSWORD)
        yag.send(
            to=recipient_email,
            subject="Purchase Information",
            contents=f"Hello,\n\nHere is the purchase information:\n\n{message}\n\nRegards,\n{SENDER_EMAIL}"
        )
        return True  # Indicate success
    except Exception as e:
        print(f"Error while sending email: {e}")
        return False  # Indicate failure

# Streamlit Dashboard
st.title("Dashboard for Purchase Records")

# Input Fields
name = st.text_input("Name of the Person")
location = st.text_input("Location Name")
object_type = st.selectbox("Type of Object", ["Transmitter", "Receiver", "Modem", "Controller"])

# Save Button
if st.button("Save"):
    if name and location and object_type:
        save_to_excel([{"Name": name, "Location": location, "Object Type": object_type}])
        st.success("Data saved successfully.")
    else:
        st.error("Please fill all fields before saving.")

# Send Button
if st.button("Send"):
    data = read_from_excel()
    if not data.empty:
        success = send_email(data, RECEIVER_EMAIL)
        if success:
            st.success("Email sent successfully.")
        else:
            st.error("Failed to send email. Check your email configuration.")
    else:
        st.error("No data to send. Please save some data first.")

# Edit Section
st.header("Edit Saved Data")
data = read_from_excel()
if not data.empty:
    edited_data = st.data_editor(data, num_rows="dynamic", use_container_width=True)
    if st.button("Save Changes"):
        edited_data.to_excel("data.xlsx", index=False)
        st.success("Changes saved successfully.")
else:
    st.info("No data available to edit.")

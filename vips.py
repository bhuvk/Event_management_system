import streamlit as st
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
import subprocess
import pandas as pd
import guests

def insert_vip(conn):
    
    cursor=conn.cursor()
    guests.view_guest_list(conn)
    guest_id_to_mark_vip = st.number_input("Enter the ID of the guest to mark as VIP:")

    vip_name = st.text_input("Enter VIP name:")
    designation = st.text_input("Enter designation:")
    age = st.number_input("Enter age:")
    phone_number = st.text_input("Enter phone number:")

    if st.button("Mark as VIP"):
        # Use SQL INSERT query to add the VIP information to the VIP table
        insert_query = '''
            INSERT INTO VIPs (GUEST_ID, vip_NAME, DESIGNATION, AGE, PHONE_No)
            VALUES (%s, %s, %s, %s, %s)
        '''

        try:
            # Execute the SQL query with the guest ID and additional VIP information
            cursor.execute(insert_query, (guest_id_to_mark_vip, vip_name, designation, age, phone_number))
            conn.commit()
            st.success(f"Guest with ID {guest_id_to_mark_vip} marked as VIP successfully!")
        except mysql.connector.Error as e:
            st.error(f"Error marking guest as VIP: {e}")


def view_vip_list(conn):
    cursor=conn.cursor()
    select_query = "SELECT * FROM vips"
    cursor.execute(select_query)

    # Fetch all rows from the result set
    guest_data = cursor.fetchall()

    # Check if there is data to display
    if guest_data:
        # Convert the result set to a Pandas DataFrame
        df = pd.DataFrame(guest_data, columns=[desc[0] for desc in cursor.description])

        # Display the DataFrame using Streamlit
        st.dataframe(df)
    else:
        st.warning("No guest data found.")
        
def delete_vip_by_guest_id(conn):
    # Create a cursor to execute SQL queries
    cursor = conn.cursor()

    # Streamlit form to get user input
    guest_id_to_delete_vip = st.number_input("Enter the ID of the guest to remove from VIP list:")

    if st.button("Remove from VIP"):
        # Use SQL DELETE query to remove the guest from the VIP table
        delete_query = "DELETE FROM VIPs WHERE GUEST_ID = %s"

        try:
            # Execute the SQL query with the guest ID
            cursor.execute(delete_query, (guest_id_to_delete_vip,))
            conn.commit()
            st.success(f"Guest with ID {guest_id_to_delete_vip} removed from VIP list successfully!")
        except mysql.connector.Error as e:
            st.error(f"Error removing guest from VIP list: {e}")
            
def update_vip_details(conn):
    cursor = conn.cursor()

    st.subheader("Update VIP Details")

    # Get the VIP name to update
    vip_name_to_update = st.text_input("Enter the VIP name to update:")

    if vip_name_to_update:
        # Check if the VIP name exists
        check_query = "SELECT * FROM VIPs WHERE VIP_NAME = %s"
        cursor.execute(check_query, (vip_name_to_update,))
        existing_vip = cursor.fetchone()

        if existing_vip:
            st.write(f"\n\n**Existing VIP Details:**")
            st.write(f"VIP Name: {existing_vip[1]}, Designation: {existing_vip[2]}, Age: {existing_vip[3]}, Phone: {existing_vip[4]}")

            # Update form
            st.write("\n\n**Update Form:**")
            updated_designation = st.text_input("Updated Designation:", value=existing_vip[3])
            updated_age = st.number_input("Updated Age:", value=existing_vip[4], min_value=0)
            updated_phone = st.text_input("Updated Phone Number:", value=existing_vip[2])

            if st.button("Update VIP Details"):
                # Update the VIP details in the database
                update_query = "UPDATE VIPs SET DESIGNATION = %s, AGE = %s, PHONE_No = %s WHERE VIP_NAME = %s"
                cursor.execute(update_query, (updated_designation, updated_age, updated_phone, vip_name_to_update))
                conn.commit()
                st.success("VIP details updated successfully!")

        else:
            st.warning("VIP not found.")
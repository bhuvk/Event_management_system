import streamlit as st
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
import subprocess
import pandas as pd


def insert_data_to_guests(conn, xml_file_path):
    cursor = conn.cursor()

    # Parse the XML file
    xml_tree = ET.parse(xml_file_path)
    xml_root = xml_tree.getroot()

    for row in xml_root.findall('.//ROW'):
        guest_data = {
            'GUEST_ID': row.find('GUEST_ID').text,
            'GUEST_NAME': row.find('GUEST_NAME').text,
            'ADDRESS_LINE_1': row.find('ADDRESS_LINE_1').text,
            'ADDRESS_LINE_2': row.find('ADDRESS_LINE_2').text,
            'CLIENT_ID': row.find('CLIENT_ID').text,
        }

        # SQL INSERT query
        insert_query = '''
            INSERT INTO GUESTS (GUEST_ID, GUEST_NAME, ADDRESS_LINE_1, ADDRESS_LINE_2, CLIENT_ID)
            VALUES (%(GUEST_ID)s, %(GUEST_NAME)s, %(ADDRESS_LINE_1)s, %(ADDRESS_LINE_2)s, %(CLIENT_ID)s)
        '''

        try:
            # Execute the SQL query
            cursor.execute(insert_query, guest_data)
            conn.commit()
            st.success(f"Data inserted successfully for GUEST_ID: {guest_data['GUEST_ID']}")
        except mysql.connector.Error as e:
            st.error(f"Error inserting data: {e}")

def update_guest_list(conn):
    cursor=conn.cursor()
    view_guest_list(conn)
    guest_name_to_update = st.text_input("Enter guest name to update:")

    # Execute a SELECT query to retrieve guest data for the specified name
    select_query = "SELECT * FROM GUESTS WHERE GUEST_NAME = %s"
    cursor.execute(select_query, (guest_name_to_update,))
    guest_data = cursor.fetchone()

    if guest_data:
        # Display current details of the selected guest
        st.write("\n\n**Current Guest Details:**")
        st.write(f"ID: {guest_data[0]}, Name: {guest_data[1]}, Address Line 1: {guest_data[2]}, "
                f"Address Line 2: {guest_data[3]}, Client ID: {guest_data[4]}")

        # Streamlit form to get updated details from the user
        updated_address_line_1 = st.text_input("Enter updated Address Line 1:", guest_data[2])
        updated_address_line_2 = st.text_input("Enter updated Address Line 2:", guest_data[3])

        if st.button("Update Guest Details"):
            # Use SQL UPDATE query to update guest details
            update_query = "UPDATE GUESTS SET ADDRESS_LINE_1 = %s, ADDRESS_LINE_2 = %s WHERE GUEST_NAME = %s"

            try:
                # Execute the SQL query with the updated details and guest name
                cursor.execute(update_query, (updated_address_line_1, updated_address_line_2, guest_name_to_update))
                conn.commit()
                st.success(f"Details for guest '{guest_name_to_update}' updated successfully!")
            except mysql.connector.Error as e:
                st.error(f"Error updating guest details: {e}")
    else:
        st.warning(f"No guest found with the name '{guest_name_to_update}'.")
    
def view_guest_list(conn):
    cursor=conn.cursor()
    select_query = "SELECT * FROM GUESTS"
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

def delete_guests(conn):
    cursor=conn.cursor()
    view_guest_list(conn)
    guest_name_to_delete = st.text_input("Enter guest name to delete:")

    if st.button("Delete Guests"):
        # Use SQL DELETE query to delete guests by name
        delete_query = "DELETE FROM GUESTS WHERE GUEST_NAME = %s"

        try:
            # Execute the SQL query with the guest name
            cursor.execute(delete_query, (guest_name_to_delete,))
            conn.commit()
            st.success(f"Guests with name '{guest_name_to_delete}' deleted successfully!")
        except mysql.connector.Error as e:
            st.error(f"Error deleting guests: {e}")
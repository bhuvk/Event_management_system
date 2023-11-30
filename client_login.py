import streamlit as st
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
import subprocess
import pandas as pd
def get_client_details(cursor, client_id):
    # Fetch client details based on the entered ID
    get_client_query = "SELECT * FROM clients WHERE client_id = %s"
    cursor.execute(get_client_query, (client_id,))
    return cursor.fetchone()

def enter_client_data(conn):
    cursor=conn.cursor()
    client_name = st.text_input("Client Name:")
    address_line_1 = st.text_input("Addr Line 1:")
    address_line_2 = st.text_input("Address Line 2:")
    address_line_3 = st.text_input("Address Line 3:")
    budget = st.number_input("Budget for Event( in Rs.):", min_value=0.0)
    bill_no = st.number_input("Bill Number:", min_value=1, step=1)

    if st.button("Submit"):
        update_data_query = '''
            INSERT INTO clients(client_name, address_line_1, address_line_2, address_line_3, budget, bill_no)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        data = (client_name, address_line_1, address_line_2, address_line_3, 
                budget, bill_no)
        cursor.execute(update_data_query, data)
        conn.commit()
        st.success("Data submitted successfully! kindly note your Client ID:")
        last_inserted_id = cursor.lastrowid
        st.write(f"Your Client ID is: {last_inserted_id}")

def view_tables(conn):
    cursor= conn.cursor()
    selected_client_id_view = st.number_input("Enter Client ID:",min_value=1)
    query = 'SELECT * FROM CLIENTS where client_id =%s'
    cursor.execute(query, (selected_client_id_view,))
    new_name=st.text_input("Enter your Name to verify its you")
    # Fetch the result
    result = cursor.fetchone()
    selected_client_view = get_client_details(cursor, selected_client_id_view)
    # Check if a result is found
    if result and new_name==selected_client_view[1]:
        # Convert the result to a DataFrame
        df = pd.DataFrame([result], columns=[desc[0] for desc in cursor.description])

        # Display the DataFrame
        st.dataframe(df)
    elif selected_client_view and new_name != selected_client_view[1]:
            st.error("check your name!")
    else:
        st.warning(f"No data found for client ID: {selected_client_id_view}")
    
def delete_client_data(conn):
    
    cursor=conn.cursor()
    selected_client_id_delete = st.number_input("Enter Client ID to delete:",min_value=1)
    new_name=st.text_input("Enter your Name to verify its you")
    if selected_client_id_delete:
        selected_client_delete = get_client_details(cursor, selected_client_id_delete)

        if selected_client_delete and new_name == selected_client_delete[1]:
            st.write(f"\n\n**Selected Client Details to Delete:**")
            st.write(f"ID: {selected_client_delete[0]}, client_Name: {selected_client_delete[1]}, "
            f"Address: {selected_client_delete[2]}, {selected_client_delete[3]}, {selected_client_delete[4]}, "
            f"Budget: {selected_client_delete[5]}, Bill Number: {selected_client_delete[6]}")

            if st.button("Delete Client"):
                delete_data_query = "DELETE FROM clients WHERE client_id = %s"
                cursor.execute(delete_data_query, (selected_client_id_delete,))
                conn.commit()
                st.success("Client details deleted successfully!")
        elif selected_client_delete and new_name != selected_client_delete[1]:
            st.error("check your name!")
        else:
            st.warning("Client not found.")


def update_client_data(conn):
    cursor=conn.cursor()
    selected_client_id_update = st.number_input("Enter Client ID to update:", min_value=1)
    new_name=st.text_input("Enter your Name to verify its you")
    if selected_client_id_update:
        
        # Fetch client details based on the entered ID
        get_client_query = "SELECT * FROM clients WHERE client_id = %s"
        cursor.execute(get_client_query, (selected_client_id_update,))
        selected_client_update = cursor.fetchone()

        if selected_client_update and new_name == selected_client_update[1]:
            st.write(f"\n\n**Selected Client Details to Update:**")
            #st.write(f"ID: {selected_client_update[0]}, client_Name: {selected_client_update[1]}, "
                    #f"Address: {selected_client_update[2]}, {selected_client_update[3]}, {selected_client_update[4]}, "
                    #f"Budget: {selected_client_update[5]}, Bill Number: {selected_client_update[6]}")
            #st.dataframe(selected_client_update)

            # Input fields for updating data
            new_name = st.text_input("Enter new name:", selected_client_update[1])
            new_address = st.text_input("Enter new address:", selected_client_update[2])
            new_budget= st.text_input("Enter new budget:", selected_client_update[5])
            # Add other input fields for updating other columns

            if st.button("Update My Details"):
                # Update data in the clients table
                update_data_query = "UPDATE clients SET client_Name = %s, address_line_1 = %s,BUDGET=%s WHERE client_id = %s"
                cursor.execute(update_data_query, (new_name, new_address,new_budget, selected_client_id_update))
                conn.commit()
                st.success("Client details updated successfully!")
        elif selected_client_update and new_name != selected_client_update[1]:
            st.error("check your name!")
        else:
            st.warning("Client not found.")





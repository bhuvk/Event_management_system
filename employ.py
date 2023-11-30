import streamlit as st
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
import pandas as pd

def execute_query(cursor, query, values=None):
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        return True
    except mysql.connector.Error as e:
        st.error(f"Error executing query: {e}")
        return False

def get_employee_names(conn):
    cursor = conn.cursor()
    query = 'SELECT DESIGNATION FROM EMPLOYEES'
    if execute_query(cursor, query):
        result = cursor.fetchall()
        employee_names = [row[0] for row in result]
        return employee_names
    else:
        return []
    
def display_employee_table(conn):
    cursor = conn.cursor()
    query = 'SELECT * FROM EMPLOYEES'
    if execute_query(cursor, query):
        result = cursor.fetchall()
        if result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            st.subheader("Employee Table")
            st.dataframe(df)
        else:
            st.warning("No data found in the EMPLOYEES table.")
def choose_manager(conn):
    cursor = conn.cursor()

    # Display the employee table
    display_employee_table(conn)

    # Ask the client to choose a manager
    manager_name = st.selectbox("Choose your manager:", get_employee_names(conn))

    return manager_name

def insert_into_event_managed_by(conn):
    cursor = conn.cursor()
    event_id=st.text_input("enter event id")
    # Get the manager's employee number based on the name
    manager_query = 'SELECT EMPLOYEE_NO FROM EMPLOYEES'
    cursor.execute(manager_query)
    manager_result = cursor.fetchall()

    if manager_result:
        employee_no = manager_result[0]

        # Insert into EVENT_MANAGED_BY table
        insert_query = 'INSERT INTO EVENT_MANAGED_BY (EVENT_ID,EMPLOYEE_NO) VALUES (%s, %s)'
        cursor.execute(insert_query, (event_id, employee_no,))
        conn.commit()
        st.success("Manager assigned to the event successfully!")
    else:
        st.warning("Manager not found.")

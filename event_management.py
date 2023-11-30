import streamlit as st
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
import events
import client_login
import decors
import guests
import subprocess
import vips
import dash
import employ
import pandas as pd
# Define a SessionState class to persist the connection state
class SessionState:
    def __init__(self):
        self.conn = None
        self.data_inserted = False

# Function to connect to the database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bhuvan@123",
            database="evem",
            auth_plugin='mysql_native_password'
        )

        # Check and create tables if not exist
        #check_and_create_tables(conn)

        return conn

    except mysql.connector.Error as e:
        print(e)

    return None


    

def check_and_create_tables(conn):
    try:
        cursor = conn.cursor()

        # Check if 'clients' table exists
        cursor.execute("SHOW TABLES LIKE 'clients'")
        if not cursor.fetchone():
            create_clients_table(cursor)

        # Check if 'guests' table exists
        cursor.execute("SHOW TABLES LIKE 'guests'")
        if not cursor.fetchone():
            create_guests_table(cursor)

        # Check if 'VIPs' table exists
        cursor.execute("SHOW TABLES LIKE 'VIPs'")
        if not cursor.fetchone():
            create_VIPs_table(cursor)

        # Check if 'Venues' table exists
        cursor.execute("SHOW TABLES LIKE 'venues'")
        if not cursor.fetchone():
            create_venues_table(cursor)

        # Check if 'events' table exists
        cursor.execute("SHOW TABLES LIKE 'events'")
        if not cursor.fetchone():
            create_events_table(cursor)

        # Check if 'employees' table exists
        cursor.execute("SHOW TABLES LIKE 'employees'")
        if not cursor.fetchone():
            create_employees_table(cursor)
        cursor.close()

        # Check if 'DECORATORS' table exists
        cursor.execute("SHOW TABLES LIKE 'decorators'")
        if not cursor.fetchone():
            create_decorators_table(cursor)

        # Check if 'caterers' table exists
        cursor.execute("SHOW TABLES LIKE 'caterers'")
        if not cursor.fetchone():
            create_caterers_table(cursor)

        # Check if 'event_managed_by' table exists
        cursor.execute("SHOW TABLES LIKE 'event_managed_by'")
        if not cursor.fetchone():
            create_event_managed_by_table(cursor)
        
        # Check if 'clients' table exists
        cursor.execute("SHOW TABLES LIKE 'clients'")
        if not cursor.fetchone():
            create_clients_table(cursor)

        # Check if 'guests' table exists
        cursor.execute("SHOW TABLES LIKE 'guests'")
        if not cursor.fetchone():
            create_guests_table(cursor)

        # Check if 'VIPs' table exists
        cursor.execute("SHOW TABLES LIKE 'VIPs'")
        if not cursor.fetchone():
            create_VIPs_table(cursor)
        
        
        
    except mysql.connector.Error as e:
        st.error(f"Error checking and creating tables: {e}")

def call_get_event_summary(conn, event_id):
    cursor = conn.cursor()

    try:
        # Call the stored procedure
        cursor.callproc("get_event_summary", [event_id])

        # Fetch the results
        for result in cursor.stored_results():
            # Assuming you want to display the results in Streamlit
            result_data = result.fetchall()
            columns = result.column_names
            df = pd.DataFrame(result_data, columns=columns)
            
            # Display the DataFrame in Streamlit
            st.dataframe(df)
            
    except mysql.connector.Error as e:
        st.error(f"Error calling stored procedure: {e}")
        
def main():
    st.set_page_config(page_title="Event Management System", page_icon=":computer:")

    # Apply custom styling to the title
    st.title("Welcome to Our Event Management System")
    st.markdown(
        "<style>"
        "h1 { color: blue; text-align: center; font-size: 36px; }"
        "</style>",
        unsafe_allow_html=True,
    )

    # Add a colorful and elegant background
    st.markdown(
        """
        <style>
        body {
            background-color: red /* Light gray background */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    #st.markdown(""" 
                ##""")
    # Initialize or retrieve session state
    session_state = SessionState()

    if not session_state.conn:
        # If connection is not established, connect to the database
        session_state.conn = connect_to_database()

    if session_state.conn:
        rad= st.sidebar.radio("NAVIGATION",["DASHBOARD","CLIENT DETAILS","EVENT INFORMATION","DECORATORS","GUESTS","VIPS","CATERERS","EMPLOYEES"])
        if rad== "DASHBOARD":
            st.subheader("Welcome to your Dashboard")
            cursor = session_state.conn.cursor()
            

            # Button to trigger the stored procedure call
            if st.button("Get Event Summary"):
                cursor.execute("CALL get_event_details()")
    
    # If the procedure returns results, you can fetch them
                result = cursor.fetchall()
                st.write("Result from stored procedure:")
                st.write(result)
            #call_get_event_summary(session_state.conn, event_id)
            df_dashboard = dash.get_dashboard_info(session_state.conn)

            # Display the dashboard table
            st.subheader("Event Details, Decorator, Caterer, and Venue Information")
            if not df_dashboard.empty:
                st.dataframe(df_dashboard)
            dash.display_events_by_client_name(session_state.conn)
            dash.display_events_by_venue_type(session_state.conn)
            dash.display_top_caterers(session_state.conn)
            st.subheader("BUGDET SPENT SO FAR")
            event_id=st.text_input("enter event id",placeholder="1")
            dash.calculate_total_budget(session_state.conn,event_id)
            
            
        if rad== "CLIENT DETAILS":
            menu_options = ["---","Enter My details", "View My details", "Update My details", "Delete My details"]
            choice= st.selectbox("Select an option", menu_options)
            if choice == "Enter My details":
                client_login.enter_client_data(session_state.conn)
            elif choice == "View My details":
                client_login.view_tables(session_state.conn)
            elif choice == "Update My details":
                client_login.update_client_data(session_state.conn)
            elif choice == "Delete My details":
                client_login.delete_client_data(session_state.conn)
            #subprocess.run(["streamlit","run","client_login.py"])
            
        if rad=="EVENT INFORMATION":
            menu_options = ["---","Enter Event details", "View Event details", "Update existing Event details", "Delete Existing event details"]
            choice= st.selectbox("Select an option", menu_options)
            if choice == "Enter Event details":
                events.enter_event_data(session_state.conn)
            elif choice == "View Event details":
                events.view_event(session_state.conn)
            elif choice == "Update existing Event details":
                events.update_event_data(session_state.conn)
            elif choice == "Delete Existing event details":
                events.delete_event_data(session_state.conn)
            #events.event_stuff(session_state.conn)
        
        if rad=="DECORATORS":
            decors.decor_stuff(session_state.conn)
            
        if rad=="GUESTS":
            
            but=st.selectbox("select your operation",["---","insert guest list","update guest list","view guest list","delete guest list"])
            if but=="insert guest list":
                if st.button("insert guest"):
                    guests.insert_data_to_guests(session_state.conn,"/Users/bhuvanvijaykumar/Documents/SEM V/.vscode/DBMS/guests.xml")
            if but=="view guest list":
                guests.view_guest_list(session_state.conn)
            if but=="delete guest list":
                guests.delete_guests(session_state.conn)
            if but=="update guest list":
                guests.update_guest_list(session_state.conn)
        
        if rad=="VIPS":
            but=st.selectbox("select your operation",["---","insert vip ","update vip details","view vip list","delete vip"])
            if but=="insert vip ":
                vips.insert_vip(session_state.conn)
            if but=="view vip list":
                vips.view_vip_list(session_state.conn)
            if but=="delete vip":
                vips.delete_vip_by_guest_id(session_state.conn)
            if but=="update vip details":
                vips.update_vip_details(session_state.conn)
        if rad=="CATERERS":
            decors.caterer_stuff(session_state.conn)
        
        if rad=="EMPLOYEES":
            employ.insert_into_event_managed_by(session_state.conn)
    # Close the connection when the Streamlit app is closed
    if session_state.conn:
        session_state.conn.close()

if __name__ == "__main__":
    main()
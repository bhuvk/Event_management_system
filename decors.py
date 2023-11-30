import streamlit as st
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
import subprocess
import pandas as pd

import streamlit as st
import mysql.connector
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

def view_client_events(conn, client_id):
    cursor = conn.cursor()

    query = 'SELECT EVENT_ID, EVENT_NAME FROM EVENTS WHERE CLIENT_ID = %s'
    if execute_query(cursor, query, (client_id,)):
        events_result = cursor.fetchall()

        if events_result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(events_result, columns=columns)

            st.subheader("Events Hosted by the Client")
            selected_event_name = st.selectbox("Select an Event:", df['EVENT_NAME'])
            selected_event_id = df[df['EVENT_NAME'] == selected_event_name]['EVENT_ID'].values[0]
            return selected_event_id
        else:
            st.warning("No events found for the client.")
            return None

def update_decorator_for_event(conn, event_id, decorator_name, client_id):
    cursor = conn.cursor()
    event_id = int(event_id)
    client_id = int(client_id)

    # Check if the entry already exists
    check_query = 'SELECT * FROM EVENT_DECORATED_BY WHERE EVENT_ID = %s AND CLIENT_ID = %s'
    cursor.execute(check_query, (event_id, client_id))
    existing_entry = cursor.fetchone()

    if existing_entry:
        # Entry exists, update the COMPANY_NAME
        update_query = 'UPDATE EVENT_DECORATED_BY SET COMPANY_NAME = %s WHERE EVENT_ID = %s AND CLIENT_ID = %s'
        cursor.execute(update_query, (decorator_name, event_id, client_id))
        cursor.fetchone()
        conn.commit()
        st.success("Event decorator updated successfully!")
    else:
        # Entry does not exist, insert a new one
        insert_query = 'INSERT INTO EVENT_DECORATED_BY (EVENT_ID, COMPANY_NAME, CLIENT_ID) VALUES (%s, %s, %s)'
        cursor.execute(insert_query, (event_id, decorator_name, client_id))
        conn.commit()
        st.success("Event decorator added successfully!")
def remove_decorator_preference(conn, event_id, decorator_name, client_id):
    cursor = conn.cursor()

    # Check if the entry exists for the specified event and client
    check_query = 'SELECT * FROM EVENT_DECORATED_BY WHERE EVENT_ID = %s AND COMPANY_NAME = %s AND CLIENT_ID = %s'
    cursor.execute(check_query, (event_id, decorator_name, client_id))
    existing_entry = cursor.fetchone()

    if existing_entry:
        # Entry exists, remove the preference
        delete_query = 'DELETE FROM EVENT_DECORATED_BY WHERE EVENT_ID = %s AND COMPANY_NAME = %s AND CLIENT_ID = %s'
        cursor.execute(delete_query, (event_id, decorator_name, client_id))
        conn.commit()
        st.success("Decorator preference removed successfully!")
    else:
        st.error("Decorator preferences not found.")

def decor_stuff(conn):
    cursor = conn.cursor()

    st.title('Client Decorator Preferences')
    client_id = st.text_input("Enter your client id")

    selected_event_id = view_client_events(conn, client_id)

    if selected_event_id:
        query = 'SELECT * FROM DECORATORS'
        if execute_query(cursor, query):
            result = cursor.fetchall()

            if result:
                columns = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(result, columns=columns)

                st.subheader("Decorators Table")
                st.dataframe(df)
            else:
                st.warning("No data found in the DECORATORS table.")

            decorator_name = st.text_input("Enter Decorator Name:")

            if decorator_name:
                check_query = 'SELECT * FROM DECORATORS WHERE COMPANY_NAME = %s'
                if execute_query(cursor, check_query, (decorator_name,)):
                    existing_decorator = cursor.fetchone()

                    if existing_decorator:
                        st.write(f"Selected Decorator: {existing_decorator}")
                        selected_event_id = int(selected_event_id)
                        client_id = int(client_id)

                        query = 'INSERT INTO EVENT_DECORATED_BY (EVENT_ID, COMPANY_NAME, CLIENT_ID) VALUES (%s, %s, %s)'
                    
                    else:
                        st.warning("Decorator name not found.")
                    
                else:
                    st.warning("Error checking decorator name.")
                if st.button("update"):
                    update_decorator_for_event(conn, selected_event_id, decorator_name,client_id)
                    
                        #add_preferences_for_event(conn, decorator_name, selected_event_id, client_id)
                if st.button("delete"):
                    remove_decorator_preference(conn,selected_event_id,decorator_name,client_id)
            else:
                st.warning("Please enter a Decorator name.")


        
def get_caterers(conn):
    cursor = conn.cursor()
    query_caterers = 'SELECT * FROM CATERERS'
    df_caterers = pd.read_sql(query_caterers, conn)
    return df_caterers

# Function to update event caterer
def update_event_caterer(conn, selected_event_id, selected_caterer_id):
    cursor = conn.cursor()

    # Check if the entry already exists
    check_query = 'SELECT * FROM EVENT_CATERED_BY WHERE EVENT_ID = %s AND CATERER_ID = %s'
    cursor.execute(check_query, (selected_event_id, selected_caterer_id))
    existing_entry = cursor.fetchone()

    if existing_entry:
        # Entry exists, update the caterer_name
        update_query = 'UPDATE EVENT_CATERED_BY SET WHERE EVENT_ID = %s AND CATERER_ID = %s'
        cursor.execute(update_query, (selected_event_id, selected_caterer_id))
        conn.commit()
        st.success("Event caterer updated successfully!")
    else:
        # Entry does not exist, insert a new one
        insert_query = 'INSERT INTO EVENT_CATERED_BY (EVENT_ID, CATERER_ID) VALUES (%s, %s)'
        cursor.execute(insert_query, (selected_event_id, selected_caterer_id))
        conn.commit()
        st.success("Event caterer added successfully!")

def delete_event_caterer(conn, selected_event_id, selected_caterer_id):
    cursor = conn.cursor()
    selected_event_id = int(selected_event_id)
    selected_caterer_id = int(selected_caterer_id)

    # Check if the entry exists
    check_query = 'SELECT * FROM EVENT_CATERED_BY WHERE EVENT_ID = %s AND CATERER_ID = %s'
    cursor.execute(check_query, (selected_event_id, selected_caterer_id))
    existing_entry = cursor.fetchone()

    if existing_entry:
        # Entry exists, delete the row
        delete_query = 'DELETE FROM EVENT_CATERED_BY WHERE EVENT_ID = %s AND CATERER_ID = %s'
        cursor.execute(delete_query, (selected_event_id, selected_caterer_id))
        conn.commit()
        st.success("Event caterer deleted successfully!")
    else:
        st.warning("Event caterer not found.")

def caterer_stuff(conn):
    # Fetch all rows from the CATERERS table
    cursor=conn.cursor()
    df_caterers = get_caterers(conn)
    client_id = st.text_input("Enter your client id")

    selected_event_id = view_client_events(conn, client_id)
    if not df_caterers.empty:
    # Display the DataFrame using Streamlit
        st.dataframe(df_caterers)
    else:
        st.warning("No data found in the CATERERS table.")
    # Check if any results are found
    if not df_caterers.empty:
        # Display the DataFrame using Streamlit
        st.subheader("Caterers Table")
        selected_caterer_name = st.selectbox("Select a Caterer:", df_caterers['CATERER_NAME'])
        selected_caterer_id = df_caterers[df_caterers['CATERER_NAME'] == selected_caterer_name]['CATERER_ID'].values[0]

        # Ask the client to choose an event
        selected_event_id = int(st.number_input("Enter Event ID to update with selected caterer:", min_value=1))
        selected_caterer_id=int(selected_caterer_id)
        if st.button("Update Event Caterer"):
            # Update the EVENTS_CATERED_BY table with the client's preferences
            update_event_caterer(conn, selected_event_id, selected_caterer_id)
            
        if st.button("delete event caterers"):
            delete_event_caterer(conn,selected_event_id,selected_caterer_id)

    else:
        st.warning("No data found in the CATERERS table.")
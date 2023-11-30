import streamlit as st
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
import pandas as pd


def get_dashboard_info(conn):
    cursor = conn.cursor()

    # Fetch event details
    query = '''
        SELECT
            E.EVENT_ID,
            E.EVENT_NAME,
            E.EVENT_TYPE,
            E.EVENT_SYNOPSIS,
            V.VENUE_ID,
            V.VENUE_TYPE,
            V.ACCOMMODATION_QUANTITY,
            V.PRICE,
            D.COMPANY_NAME AS DECORATOR_NAME,
            C.CATERER_NAME
        FROM EVENTS E
        LEFT JOIN EVENT_DECORATED_BY ED ON E.EVENT_ID = ED.EVENT_ID
        LEFT JOIN DECORATORS D ON ED.COMPANY_NAME = D.COMPANY_NAME
        LEFT JOIN EVENT_CATERED_BY EC ON E.EVENT_ID = EC.EVENT_ID
        LEFT JOIN CATERERS C ON EC.CATERER_ID = C.CATERER_ID
        LEFT JOIN VENUES V ON E.VENUE_ID = V.VENUE_ID
    '''
    cursor.execute(query)
    result = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    df_dashboard = pd.DataFrame(result, columns=columns)
    
    return df_dashboard

def get_events_by_client_name(conn, client_name):
    cursor = conn.cursor()
    # Execute the nested query
    query = f'''
        SELECT event_name
        FROM Events
        WHERE client_id = (
            SELECT client_id
            FROM CLIENTS
            WHERE client_name = '{client_name}'
        )
    '''
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchall()

    # Return the result
    return result

# Streamlit app
def display_events_by_client_name(conn):
    st.subheader("Display Events by Client Name (Nested)")

    # Input for client name
    client_name = st.text_input("Enter Client Name:")

    # Button to execute the query
    if st.button("Get Events"):
        # Call the function to get events by client name
        events_result = get_events_by_client_name(conn, client_name)

        # Display the result using Streamlit
        if events_result:
            st.success("Events found:")
            for event in events_result:
                st.write(event[0])
        else:
            st.warning("No events found for the specified client name.")

def get_events_by_venue_type(conn, venue_type):
    cursor = conn.cursor()

    # Execute the SQL query
    query = f'''
        SELECT event_name
        FROM Events
        WHERE client_id IN (
            SELECT DISTINCT client_id
            FROM Events
            WHERE venue_id IN (
                SELECT venue_id
                FROM VENUES
                WHERE venue_type = '{venue_type}'
            )
        )
    '''

    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchall()

    # Return the result
    return result

# Streamlit app
def display_events_by_venue_type(conn):
    st.subheader("Display Events by Venue Type (Nested)")

    # Input for venue type
    venue_type = st.text_input("Enter Venue Type:")

    # Button to execute the query
    if st.button("Get event based on venue type"):
        # Call the function to get events by venue type
        events_result = get_events_by_venue_type(conn, venue_type)

        # Display the result using Streamlit
        if events_result:
            st.success("Events found:")
            for event in events_result:
                st.write(event[0])
        else:
            st.warning("No events found for the specified venue type.")
            
def get_top_caterers(conn, limit=3):
    cursor = conn.cursor()

    # Execute the SQL query
    query = f'''
        SELECT CATERERS.CATERER_NAME, COUNT(*) AS EVENT_COUNT
        FROM CATERERS
        JOIN EVENT_CATERED_BY ON CATERERS.CATERER_ID = EVENT_CATERED_BY.CATERER_ID
        GROUP BY CATERERS.CATERER_NAME
        ORDER BY EVENT_COUNT DESC
        LIMIT {limit};
    '''

    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchall()

    # Return the result
    return result

# Streamlit app
def display_top_caterers(conn):
    st.subheader("Top Caterers by Event Count (Aggregate)")

    # Input for limit
    limit = st.number_input("Enter the number of top caterers to display:", min_value=1, value=3)

    # Button to execute the query
    if st.button("Get Top Caterers"):
        # Call the function to get top caterers
        top_caterers_result = get_top_caterers(conn, limit)

        # Display the result using Streamlit
        if top_caterers_result:
            st.success("Top Caterers:")
            for caterer in top_caterers_result:
                st.write(f"{caterer[0]} - Events Count: {caterer[1]}")
        else:
            st.warning("No data found for the specified query.")
            
            
            
def calculate_total_budget(conn, event_id):
    cursor = conn.cursor()
    #st.subheader("the budget spent so far")
    try:
        # Execute the SELECT statement to call the function
        cursor.execute("SELECT calculate_total_budget(%s)", (event_id,))

        # Fetch the result of the function call
        result = cursor.fetchone()

        # Display the result
        if result:
            total_budget = result[0]
            st.success(f"Total Budget for Event {event_id}: Rs.{total_budget}")
        else:
            st.warning("Error calling calculate_total_budget function.")
    except mysql.connector.Error as e:
        st.error(f"Error calling calculate_total_budget: {e}")

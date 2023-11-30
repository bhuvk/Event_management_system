import streamlit as st
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
import subprocess
import pandas as pd

import streamlit as st
import mysql.connector
import pandas as pd


def get_caterers(conn):
    cursor = conn.cursor()
    query_caterers = 'SELECT * FROM CATERERS'
    df_caterers = pd.read_sql(query_caterers, conn)
    return df_caterers

# Function to fetch decorator data from the database
def get_decorators(conn):
    cursor = conn.cursor()
    query_decorators = 'SELECT * FROM DECORATORS'
    df_decorators = pd.read_sql(query_decorators, conn)
    return df_decorators

# Function to view client events
def view_client_events(conn, client_id):
    # Implement your view_client_events function here

# Function to update event caterer
def update_event_caterer(conn, event_id, caterer_id):
    cursor = conn.cursor()
    # Implement your update_event_caterer function here

# Streamlit app
def caterer_stuff(conn):
    st.title("Caterer and Decorator Preferences")

    # Fetch all rows from the CATERERS and DECORATORS tables
    df_caterers = get_caterers(conn)
    df_decorators = get_decorators(conn)

    # Get client ID
    client_id = st.text_input("Enter your client id")

    # View client events
    selected_event_id = view_client_events(conn, client_id)

    # Display Caterers Table
    st.subheader("Caterers Table")
    if not df_caterers.empty:
        st.dataframe(df_caterers)
    else:
        st.warning("No data found in the CATERERS table.")

    # Display Decorators Table
    st.subheader("Decorators Table")
    if not df_decorators.empty:
        st.dataframe(df_decorators)
    else:
        st.warning("No data found in the DECORATORS table.")

    # Ask the client to choose a caterer
    selected_caterer_name = st.selectbox("Select a Caterer:", df_caterers['CATERER_NAME'])
    selected_caterer_id = df_caterers[df_caterers['CATERER_NAME'] == selected_caterer_name]['CATERER_ID'].values[0]

    # Ask the client to choose an event
    selected_event_id = st.number_input("Enter Event ID to update with selected caterer:", min_value=1, value=selected_event_id)

    # Update event caterer on button click
    if st.button("Update Event Caterer"):
        selected_caterer_id = int(selected_caterer_id)
        update_event_caterer(conn, selected_event_id, selected_caterer_id)
        st.success("Event caterer updated successfully!")
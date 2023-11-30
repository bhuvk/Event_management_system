import streamlit as st
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta


def get_event_details(cursor,event_id):
    get_event_query = "SELECT * FROM events WHERE event_id = %s"
    cursor.execute(get_event_query, (event_id,))
    return cursor.fetchone()

def enter_event_data(conn):
    cursor=conn.cursor()
    event_name = st.text_input("Event Name:")
    event_type = st.text_input("Event Type:")
    event_synopsis = st.text_area("Event Synopsis:")
    if st.button("View Venues"):
        view_venue_query = 'SELECT * FROM VENUES'
        df = pd.read_sql(view_venue_query, conn)
        st.dataframe(df)
    venue_id = st.number_input("Venue ID:", min_value=1)
    event_time = st.time_input("Event Time:")
    event_date = st.date_input("Event Date:")

    client_id = st.number_input("Client ID:", min_value=1)

    if st.button("Add Event"):
        insert_data_query = '''
            INSERT INTO EVENTS (EVENT_NAME, EVENT_TYPE, EVENT_SYNOPSIS, VENUE_ID, TIME, DATE, CLIENT_ID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        data = (event_name, event_type, event_synopsis, venue_id, event_time, event_date, client_id)
        cursor.execute(insert_data_query, data)
        conn.commit()
        st.success("Event details added successfully!")

def view_event(conn):
    cursor = conn.cursor()

    query = 'SELECT EVENT_ID, EVENT_NAME, EVENT_TYPE, EVENT_SYNOPSIS, VENUE_ID, DATE, CLIENT_ID FROM EVENTS'
    cursor.execute(query)
    result = cursor.fetchall()

    # Check if any results are found
    if result:
        # Convert the result to a DataFrame
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=columns)

        # Convert the 'DATE' column to a more readable format
        df['DATE'] = pd.to_datetime(df['DATE']).dt.strftime('%Y-%m-%d')

        # Display the DataFrame using Streamlit
        st.subheader("Events")
        st.dataframe(df)
    else:
        st.warning("No data found in the EVENTS table.")


def update_event_data(conn):
    # Section for updating event details
    cursor = conn.cursor()
    st.subheader("Update Event Details")
    selected_event_id_update = st.number_input("Enter Event ID to update details:")

    if selected_event_id_update:
        get_event_query = "SELECT * FROM EVENTS WHERE EVENT_ID = %s"
        cursor.execute(get_event_query, (selected_event_id_update,))
        selected_event_update = cursor.fetchone()

        if selected_event_update:
            st.write(f"\n\n**Selected Event Details:**")
            st.write(f"ID: {selected_event_update[0]}, Name: {selected_event_update[1]}, "
                    f"Type: {selected_event_update[2]}, Synopsis: {selected_event_update[3]}, "
                    f"Venue ID: {selected_event_update[4]}, Time: {selected_event_update[5]}, "
                    f"Date: {selected_event_update[6]}, Client ID: {selected_event_update[7]}")

            # Update form
            st.write("\n\n**Update Form:**")
            event_name_update = st.text_input("Event Name:", value=selected_event_update[1])
            event_type_update = st.text_input("Event Type:", value=selected_event_update[2])
            event_synopsis_update = st.text_area("Event Synopsis:", value=selected_event_update[3])
            venue_id_update = st.number_input("Venue ID:", value=selected_event_update[4], min_value=1)
            event_date_update = st.date_input("Enter new date:", selected_event_update[6])
            #event_time_update = st.time_input("Enter new time:", selected_event_update[5])
            client_id_update = st.number_input("Client ID:", value=selected_event_update[7], min_value=1)

            if st.button("Update Event Details"):
                update_data_query = '''
                    UPDATE EVENTS
                    SET EVENT_NAME = %s, EVENT_TYPE = %s, EVENT_SYNOPSIS = %s,
                        VENUE_ID = %s, DATE = %s, CLIENT_ID = %s
                    WHERE EVENT_ID = %s
                '''
                data = (event_name_update, event_type_update, event_synopsis_update, 
                        venue_id_update, event_date_update, client_id_update, selected_event_id_update)
                cursor.execute(update_data_query, data)
                conn.commit()
                st.success("Event details updated successfully!")

        else:
            st.warning("Event not found.")

def delete_event_data(conn):
    cursor= conn.cursor()
    # Section for deleting event details
    st.subheader("Delete Event Details")
    selected_event_id_delete = st.number_input("Enter Event ID to delete:")
    if selected_event_id_delete:
            get_event_query = "SELECT * FROM EVENTS WHERE EVENT_ID = %s"
            cursor.execute(get_event_query, (selected_event_id_delete,))
            selected_event_delete = cursor.fetchone()

            if selected_event_delete:
                st.write(f"\n\n**Selected Event Details to Delete:**")
                st.write(f"ID: {selected_event_delete[0]}, Name: {selected_event_delete[1]}, "
                        f"Type: {selected_event_delete[2]}, Synopsis: {selected_event_delete[3]}, "
                        f"Venue ID: {selected_event_delete[4]}, Time: {selected_event_delete[5]}, "
                        f"Date: {selected_event_delete[6]}, Client ID: {selected_event_delete[7]}")

                if st.button("Delete Event"):
                    delete_data_query = "DELETE FROM EVENTS WHERE EVENT_ID = %s"
                    cursor.execute(delete_data_query, (selected_event_id_delete,))
                    conn.commit()
                    st.success("Event details deleted successfully!")

            else:
                st.warning("Event not found.")

    
        
import numpy as np  
import pandas as pd
import streamlit as st
import requests
from datetime import datetime, timedelta
from PIL import Image

attendance_df = pd.read_csv(r'C:\Users\LarrySang\Documents\Master DSBA\Hackthon\attendance.csv')

attendance_df_cleaned = attendance_df[attendance_df['attendance'] >= 0]

attendance_df_PortAdventuraWorld = attendance_df_cleaned[attendance_df_cleaned['FACILITY_NAME']=='PortAventura World']

attendance_df_PortAdventuraWorld['USAGE_DATE'] = pd.to_datetime(attendance_df_PortAdventuraWorld['USAGE_DATE'])

weather_data = {
    'temp': [8.33, 9.25, 10.12],
    'feels_like': [8.14, 9.02, 10.01],
    'rain_or_not': ['Yes', 'No', 'Yes']
}

df = pd.DataFrame(weather_data)



# Create data for the DataFrame
outside_schedule = {
    'Schedule': ['16h', '18h', '20h', '15h', '17h', '19h', '11h', '12h', '19h30']
}

latest_offers = {
    'Time': ['12h', '18h', '20h', '15h', '17h', '', '11h', '14h', '17h'],
    'Offers': ['Orange juice', 'beer', 'rose wine', 'small cakes', 'churros', '', 'ice cream', 'coke', 'iced tea'],
    'Special offers': ['buy 1 for 1 free', '20% discount', '10% discount', '15% discount', 'buy 5 for 1 free', '', '30% discount', '20% discount', '15% discount']
}


# Create a MultiIndex for the DataFrame
index = pd.MultiIndex.from_arrays([
    ['Row 1', 'Row 1', 'Row 1', 'Row 2', 'Row 2', 'Row 2', 'Row 3', 'Row 3', 'Row 3'],
    ['Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1']
])

index2 = pd.MultiIndex.from_arrays([
    ['Row 1', 'Row 1', 'Row 1', 'Row 2', 'Row 2', 'Row 2', 'Row 3', 'Row 3', 'Row 3'],
    ['Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1'],
    ['Row 1', 'Row 1', 'Row 1', 'Row 2', 'Row 2', 'Row 2', 'Row 3', 'Row 3', 'Row 3'],
    ['Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1', 'Column 1']
])

# Create the DataFrame
df_outside_schedule = pd.DataFrame(outside_schedule, index=('Parade', '', '', 'Performance1', '', '', 'Performance2', '', ''))
df_latest_offers = pd.DataFrame(latest_offers, index=('Bar1', '', '', 'Restuarant1', '', '', 'Stand1', '', ''))

def get_predicted_waiting_time(selected_date):
    # Assuming you have a function to retrieve predicted waiting time data
    # for each attraction on the selected date from your data source
    # Replace this with your actual implementation
    predicted_waiting_time_data = [
        ('Superman Ride', '9-19h', '30-45 minutes'),
        ('Swing Ride', '9-19h', '15-30 minutes'),
        ('Crazy Dance', '9-19h', '20-35 minutes'),
        ('Rapids Ride', '9-19h', '45-60 minutes'),
        ('Haunted House', '9-19h', '10-20 minutes')
        
    ]
    return predicted_waiting_time_data

def get_live_attraction_data(selected_date):
    # Assuming you have a function to retrieve predicted waiting time data
    # for each attraction on the selected date from your data source
    # Replace this with your actual implementation
    live_attraction_data = [
        ('Superman Ride', 'Open', '30 minutes'),
        ('Swing Ride', 'Open', '10 minutes'),
        ('Crazy Dance', 'Closed', '20 minutes'),
        ('Rapids Ride', 'Open', '45 minutes'),
        ('Haunted House', 'Open', '10 minutes')
        
    ]
    return live_attraction_data


def plan_ahead_page():
    st.title("Plan Ahead")
    # Add content for the "Plan Ahead" page
    today = datetime(2021, 8, 1)

    # Calculate the maximum allowed date (3 months from today)
    max_date = today + timedelta(days=90)
    
    selected_date = st.date_input("Choose a date within 3 months from August 1st, 2021 (including August 1st):", 
                                  min_value=today, max_value=max_date, value=today)
    
    # Loop through the original dataframe to find the expected attendance for the selected date
    expected_attendance = None
    for index, row in attendance_df_PortAdventuraWorld.iterrows():
        if row['USAGE_DATE'] == selected_date:
            expected_attendance = row['attendance']
            break
    # If expected attendance is found, determine color based on its value and display it
    if expected_attendance is not None:
        color = ""
        if expected_attendance > 50000:
            color = "red"
        elif 40000 <= expected_attendance <= 50000:
            color = "orange"
        elif 20000 <= expected_attendance < 40000:
            color = "green"
        else:
            color = "blue"
        # Display the selected date and expected attendance with color
        st.write("Selected date:", selected_date)
        st.markdown("<h2 style='font-size:16px;'>Expected Attendance/Crowd:</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color:{color}'>{expected_attendance}</h2>", unsafe_allow_html=True)
    else:
        st.write("No data available for the selected date.")
    
    st.markdown("<h2 style='font-size:16px;'>Weather Data</h2>", unsafe_allow_html=True)
    st.write("Feels Like:")
    st.write(df['feels_like'][0])
    st.write("Rain or Not:")
    st.write(df['rain_or_not'][0])

    # Retrieve predicted waiting time for each attraction on the selected day
    predicted_waiting_time = get_predicted_waiting_time(selected_date)
    
    # Convert predicted waiting time data to DataFrame for display
    df_predicted_waiting_time = pd.DataFrame(predicted_waiting_time, columns=['Attraction', 'Opening Time','Predicted Waiting Time'])
    # Set the 'Attraction' column as the index
    df_predicted_waiting_time.set_index('Attraction', inplace=True)

    # Display predicted waiting time for each attraction in a table
    st.markdown("<h2 style='font-size:16px;'>Predicted Waiting Time/Opening Time for Each Attraction on Selected Day:</h2>", unsafe_allow_html=True)
    st.write(df_predicted_waiting_time)
    st.markdown("<h2 style='font-size:16px;'>Personalized Route Planner</h2>", unsafe_allow_html=True)
    img = Image.open(r"C:\Users\LarrySang\Documents\Master DSBA\Hackthon\300x0w.jpg")
    st.image(img)

def at_the_park_page():
    st.title("At the Park")
    # Add content for the "At the Park" page
    today = datetime(2021, 8, 1)

    filtered_rows = attendance_df_PortAdventuraWorld.loc[attendance_df_PortAdventuraWorld['USAGE_DATE'] == today]
    
    # Now you can work with the filtered DataFrame
    if not filtered_rows.empty:
        real_attendance = int(filtered_rows['attendance'])
    else:
        print("No attendance data available for today.")
            
    # If expected attendance is found, determine color based on its value and display it
    if real_attendance is not None:
        color = ""
        if real_attendance > 50000:
            color = "red"
        elif 40000 <= real_attendance <= 50000:
            color = "orange"
        elif 20000 <= real_attendance < 40000:
            color = "green"
        else:
            color = "blue"
        # Display the selected date and expected attendance with color
        st.write("Current Attendance/Crowd Today:", end='')
        st.markdown(f"<h2 style='color:{color}'>{real_attendance}</h2>", unsafe_allow_html=True)
    else:
        st.write("No data available for the selected date.")

    st.markdown("<h2 style='font-size:16px;'>Live Attraction Data</h2>", unsafe_allow_html=True)

    # Convert predicted waiting time data to DataFrame for display
    live_data = get_live_attraction_data(today)
    df_live__time = pd.DataFrame(live_data, columns=['Attraction', 'Opening Status','Live Waiting Time'])
    # Set the 'Attraction' column as the index
    df_live__time.set_index('Attraction', inplace=True)

    # Display predicted waiting time for each attraction in a table
    st.markdown("<h2 style='font-size:16px;'>Predicted Waiting Time/Opening Time for Each Attraction Today:</h2>", unsafe_allow_html=True)
    st.write(df_live__time)
    st.markdown("<h2 style='font-size:16px;'>New Events</h2>", unsafe_allow_html=True)
    st.write(df_outside_schedule.style.hide())
    st.markdown("<h2 style='font-size:16px;'>Latest Offers</h2>", unsafe_allow_html=True)
    st.write(df_latest_offers.style.hide())

    st.markdown("<h2 style='font-size:16px;'>Nearby Recommendation System</h2>", unsafe_allow_html=True)
    img2 = Image.open(r"C:\Users\LarrySang\Documents\Master DSBA\Hackthon\places-nearby-details-628f9aceb68b974c644466eebe22bbc9.png")
    st.image(img2)


# Display page titles side by side
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h1 style='color:blue;'>Plan Ahead</h1>", unsafe_allow_html=True)
with col2:
    st.markdown("<h1>At the Park</h1>", unsafe_allow_html=True)

# Check which page is selected
selected_page = st.selectbox("Select a page", ["Plan Ahead", "At the Park"])

# Display content based on the selected page
if selected_page == "Plan Ahead":
    plan_ahead_page()
elif selected_page == "At the Park":
    at_the_park_page()
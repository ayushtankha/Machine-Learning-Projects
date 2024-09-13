import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt

def app():
  alt.themes.enable("dark")

  #######################
  # Load the datasets
  entity_schedule = pd.read_csv('entity_schedule.csv')
  waiting_times = pd.read_csv('waiting_times.csv')
  attendance = pd.read_csv('attendance.csv')

  link_attraction_park = pd.read_csv('link_attraction_park.csv')
  # Split the 'ATTRACTION;PARK' column into two separate columns
  link_attraction_park[['ATTRACTION', 'PARK']] = link_attraction_park['ATTRACTION;PARK'].str.split(';', expand=True)
  # Drop the original 'ATTRACTION;PARK' column
  link_attraction_park.drop(columns=['ATTRACTION;PARK'], inplace=True)

  # Filter the attractions for the park "PortAventura World"
  portaventura_attractions = link_attraction_park[link_attraction_park['PARK'] == 'PortAventura World']['ATTRACTION']

  # Filter the waiting_times dataset for rides in PortAventura World
  waiting_rides = waiting_times[waiting_times['ENTITY_DESCRIPTION_SHORT'].isin(portaventura_attractions)]
  # Filter the entity_schedule dataset for rides in PortAventura World
  rides_schedule = entity_schedule[entity_schedule['ENTITY_DESCRIPTION_SHORT'].isin(portaventura_attractions)]
  # Filter data for PortAventura World
  attendance_pa = attendance[attendance['FACILITY_NAME'] == 'PortAventura World']



  #######################
  # Plots
      
  # Line chart
  def make_lines(input_df, selected_year):
      input_df['USAGE_DATE'] = pd.to_datetime(input_df['USAGE_DATE'])
      input_df['YEAR'] = input_df['USAGE_DATE'].dt.year
      attendance_pa_year = input_df[input_df['YEAR'] == selected_year]
      attendance_per_month_year = attendance_pa_year.groupby(attendance_pa_year['USAGE_DATE'].dt.month)['attendance'].sum().reset_index()

      month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      attendance_per_month_year['Month'] = attendance_per_month_year['USAGE_DATE'].map(lambda x: month_names[x - 1])
          
      line_chart = alt.Chart(attendance_per_month_year).mark_line().encode(
          alt.X('Month:N', title='Month'),
          alt.Y('attendance:Q', title='Total Attendance'),
          tooltip=['Month:N', 'attendance:Q']
      ).properties(
          title='Attendance per Month',
          width=800,
          height=400
      )
      return line_chart

  # Bar chart
  def make_bar(input_df, selected_year):
      input_df['WORK_DATE'] = pd.to_datetime(input_df['WORK_DATE'])
      input_df['YEAR'] = input_df['WORK_DATE'].dt.year
      waiting_rides_year = input_df[input_df['YEAR'] == selected_year]
      waiting_rides_year['CAPACITY_USE_PERCENTAGE'] = (waiting_rides_year['GUEST_CARRIED'] / waiting_rides_year['CAPACITY']) * 100
      average_capacity_use_percentage_year = waiting_rides_year.groupby('ENTITY_DESCRIPTION_SHORT')['CAPACITY_USE_PERCENTAGE'].mean().reset_index()
          
      bar_chart = alt.Chart(average_capacity_use_percentage_year).mark_bar().encode(
          alt.X('ENTITY_DESCRIPTION_SHORT:N', title='Attraction'),
          alt.Y('CAPACITY_USE_PERCENTAGE:Q', title='Average Capacity Use Percentage'),
          color=alt.Color('ENTITY_DESCRIPTION_SHORT:N', legend=None)
      ).properties(
          title='Average Percentage of Capacity Use per Attraction',
          width=800,
          height=400
      ) 
      return bar_chart

  # Ex-Pie chart
  def make_bar_2(input_df, selected_year):
      input_df['WORK_DATE'] = pd.to_datetime(input_df['WORK_DATE'])
      input_df['YEAR'] = input_df['WORK_DATE'].dt.year
      waiting_rides_year = input_df[input_df['YEAR'] == 2019]
      total_guests_carried_year = waiting_rides_year.groupby('ENTITY_DESCRIPTION_SHORT')['GUEST_CARRIED'].sum().reset_index()
      percentage_guests_carried_year = (total_guests_carried_year['GUEST_CARRIED'] / total_guests_carried_year['GUEST_CARRIED'].sum()) * 100

      # Filter attractions with less than 3% of the total guests carried
      filtered_percentage_guests_carried_year = percentage_guests_carried_year[percentage_guests_carried_year >= 3]

      bar_chart_1 = alt.Chart(filtered_percentage_guests_carried_year).mark_bar().encode(
          alt.X('ENTITY_DESCRIPTION_SHORT:N', title='Attraction'),
          alt.Y('GUEST_CARRIED:Q', title='Percentage of Guests Carried'),
          color=alt.Color('ENTITY_DESCRIPTION_SHORT:N', legend=None)
      ).properties(
          title='Percentage of Guests Carried per Attraction',
          width=800,
          height=400
          
      )

      return bar_chart_1



  # Convert population to text 
  def format_number(num):
      if num > 1000000:
          if not num % 1000000:
              return f'{num // 1000000} M'
          return f'{round(num / 1000000, 1)} M'
      return f'{num // 1000} K'

  # Calculation attendance per year
  def calculate_attendance(input_df, selected_year):
    input_df.loc[:, 'USAGE_DATE'] = pd.to_datetime(input_df['USAGE_DATE'])
    input_df.loc[:, 'YEAR'] = input_df['USAGE_DATE'].dt.year
    total_attendance_year = input_df.loc[input_df['YEAR'] == selected_year, 'attendance'].sum()
    return total_attendance_year


  #######################
  # Dashboard Main Panel
  col = st.columns((1.5, 4.5), gap='medium')

  with col[0]:
      # Year select box list 
      year_list = list(['2022', '2021', '2020', '2019', '2018'])[::-1]
      selected_year = st.selectbox('Select a year', year_list)
      
      
      # Capcaity Figure & Operation 
      st.markdown('#### Capacity')
      attendance_year = calculate_attendance(attendance_pa, selected_year)
      attendance = format_number(attendance_year)
      st.metric(label="Visitors", value=attendance, delta=0)

      
      st.markdown('#### Total Revenue')
      # Assuming the average ticket price is 37.5 euros
      average_ticket_price = 37.5
      total_ticket_revenue_year = attendance_year * average_ticket_price
      tickets = format_number(total_ticket_revenue_year)
      st.metric(label="Tickets Revenue", value=tickets, delta=0)

      # Assuming the average food and beverage revenue is 12 euros
      average_food_and_beverage_price = 12
      total_food_and_beverage_revenue_year = attendance_year * average_food_and_beverage_price
      food_bev = format_number(total_food_and_beverage_revenue_year)
      st.metric(label="Food & Beverages Revenue", value=food_bev, delta=0)


  with col[1]:
      st.markdown('#### Total Number of Visitors per Year')
      line = make_lines(attendance_pa, selected_year)
      st.altair_chart(line, use_container_width=True)
      
      st.markdown('#### Operation Cost')
      bar = make_bar(waiting_rides, selected_year)
      st.altair_chart(bar, use_container_width=True)

      st.markdown('#### Attraction Popularity')
      pie = make_bar_2(waiting_rides, selected_year)
      st.altair_chart(pie, use_container_width=True)
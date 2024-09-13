import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt

import park_info, kpi_tracker

st.set_page_config(
    page_title="PortAventura - Park Manager",
    page_icon="🏂",
    layout="wide", #expand to the entirety of the wide of the page
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='Park Manager Pages ',
                options=['Park Info','Estimator','KPIs Tracking','Statistics','Other'],
                icons=['house-fill','person-circle','trophy-fill','chat-fill','info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                )

        if app == "Park Info":
            park_info.app()
        if app == "KPIs Tracking":
            kpi_tracker.app()    
             
    run()            
         

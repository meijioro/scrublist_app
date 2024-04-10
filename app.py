import streamlit as st
from streamlit_option_menu import option_menu
import scrub, everest_compare

class MultiApp:
    def __init__(self):
        self.apps = []
    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })
    def run():
        with st.sidebar:        
            app = option_menu(
                menu_title='Pondering ',
                options=['Scrub List','Remove Invalid Records'],
                styles={
                    "container": {
                            "padding": "5!important",
                            "background-color":'black'
                        },
                    "nav-link": {
                        "color":"white",
                        "margin":"0px", 
                        "--hover-color": "blue"
                        },
                    "nav-link-selected": {
                        "background-color": "#02ab21"
                    },
                })
        if app == "Scrub List":
            scrub.app()
        if app == "Remove Invalid Records":
            everest_compare.app()    
       
    run()                

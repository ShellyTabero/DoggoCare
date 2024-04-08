import streamlit as st
import env

GOOGLE_API_KEY = env.GOOGLE_API_KEY

current_profile = None
email = None

# info-dicts
rabis_dict = {"freq": 12, "interval": 'months'} # every 12 months
hexagon_dict = {"freq": 12, "interval": 'months'} # every 12 months
spirocerca_dict = {"freq": 2, "interval": 'months'} # every 2 months

profiles_dict = {}

background_link = 'https://img.freepik.com/free-vector/dog-background-with-cute-pets-illustration_53876-111990.jpg?w=360&t=st=1712073580~exp=1712074180~hmac=dd96c155d3bdd3296d9f610b9bdba4e9a956c0265b7231f1c4e5b965460564ef'
def add_bg_from_url(url):
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url({url});
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



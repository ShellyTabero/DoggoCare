import streamlit as st
import config

config.local_css("style.css")
config.add_bg_from_url(config.background_link)

st.markdown("<h1 style='text-align: center; color: black;'>DoggoCare</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Choose dog:</h1>", unsafe_allow_html=True)

if st.button("Add dog"):
    st.switch_page('welcomePage.py')
dogs = config.profiles_dict.keys()

for dog in dogs:
    if st.button(dog):
        config.current_profile = dog
        st.switch_page('pages/page4.py')
    if config.profiles_dict[dog]['image'] is not None:
        st.image(config.profiles_dict[dog]['image'], width=250)


import streamlit as st
from streamlit_extras.grid import grid
import config

st.set_page_config(initial_sidebar_state="collapsed")
config.local_css("style.css")
config.add_bg_from_url(config.background_link)


def basic_definitions(name):
    config.profiles_dict[name]['haircut'] = {"freq": None,  # User's choice from list(range(1,13))
                                                            "interval": None  # User's choice from ["weeks", "months"]
                                                            }
    config.profiles_dict[config.current_profile]['image'] = None
    config.profiles_dict[name]['walking'] = {}
    config.profiles_dict[name]['feeding'] = {}
    config.profiles_dict[name]['last_rabis'] = None
    config.profiles_dict[name]['last_hexagon'] = None
    config.profiles_dict[name]['last_spirocerca'] = None
    config.profiles_dict[name]['last_haircut'] = None
    config.profiles_dict[name]['disable_back_next'] = False


st.markdown("<h1 style='text-align: center; color: black;'>DoggoCare</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: black;'>Welcome to DoggoCare! 🐾 </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Our system will make your dog's life better! </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Please enter your dog's name to kickstart our journey:</h1>", unsafe_allow_html=True)


my_grid = grid([1,3,1],
               [1, 5, 1],
               vertical_align="bottom")

my_grid.markdown("")
name = my_grid.text_input('Name', label_visibility='hidden', placeholder='Name')
my_grid.markdown("")

if name != '':
    config.current_profile = name
    config.profiles_dict[config.current_profile] = {}
    basic_definitions(config.current_profile)
    my_grid.markdown("")
    my_grid.markdown("")
    if my_grid.button("Next"):
        st.switch_page("pages/detailsPage.py")



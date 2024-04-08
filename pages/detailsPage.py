import streamlit as st
from streamlit_extras.grid import grid
import config


config.local_css("style.css")
config.add_bg_from_url(config.background_link)

def update_details(name, breed, dob, weight, gender):
    if breed is not None:
        config.profiles_dict[name]['breed'] = breed
    if dob is not None:
        config.profiles_dict[name]['dob'] = dob
    if weight is not None:
        config.profiles_dict[name]['weight'] = weight
    if gender is not None:
        config.profiles_dict[name]['gender'] = gender

st.markdown("<h1 style='text-align: center; color: black;'>DoggoCare</h1>", unsafe_allow_html=True)

if not config.profiles_dict[config.current_profile]['disable_back_next']:
    config.profiles_dict[config.current_profile]['placeholder_lst'] = ['Breed', 'Date of Birth DD/MM/YYYY', 'Weight', 'Gender']
    placeholder_lst = config.profiles_dict[config.current_profile]['placeholder_lst']
else:
    curr_dict = config.profiles_dict[config.current_profile]
    placeholder_lst = curr_dict['placeholder_lst']
    placeholder_lst[0] = curr_dict.get('breed') if curr_dict.get('breed') else placeholder_lst[0]
    placeholder_lst[1] = curr_dict.get('dob') if curr_dict.get('dob') else placeholder_lst[1]
    placeholder_lst[2] = curr_dict.get('weight') if curr_dict.get('weight') else placeholder_lst[2]
    placeholder_lst[3] = curr_dict.get('gender') if curr_dict.get('gender') else placeholder_lst[3]

st.markdown("<h4 style='text-align: center; color: black;'>Enter some details about your dog:</h1>", unsafe_allow_html=True)

my_grid = grid([1, 3, 1], [1,3,1], [1,3,1], [1,3,1], [1,5,1], vertical_align="bottom")

# Row 2
my_grid.markdown("")
breed = my_grid.text_input('Breed', label_visibility='hidden', placeholder=placeholder_lst[0])
my_grid.markdown("")

# Row 3
my_grid.markdown("")
dob = my_grid.text_input('Date of Birth', label_visibility='hidden', placeholder=placeholder_lst[1])
my_grid.markdown("")

# Row 4
my_grid.markdown("")
weight = my_grid.text_input('Weight', label_visibility='hidden', placeholder=placeholder_lst[2])
my_grid.markdown("")

# Row 5
my_grid.markdown("")
gender = my_grid.text_input('Gender', label_visibility='hidden', placeholder=placeholder_lst[3])
my_grid.markdown("")


if config.profiles_dict[config.current_profile]['disable_back_next']:
    if my_grid.button("Main page"):
        update_details(config.current_profile, breed, dob, weight, gender)
        st.switch_page("pages/page4.py")
else:
    update_details(config.current_profile, breed, dob, weight, gender)
    my_grid.markdown("")
    my_grid.markdown("")
    if my_grid.button("Next"):
        st.switch_page("pages/page2.py")

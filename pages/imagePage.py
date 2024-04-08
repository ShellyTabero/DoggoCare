import streamlit as st
from streamlit_extras.grid import grid
import config
from PIL import Image, ImageOps

def add_border(input_image, border, color='black'):
    if input_image is not None:
        img = Image.open(input_image)
        bordered = ImageOps.expand(img, border=border, fill=color)
        return bordered

config.local_css("style.css")
config.add_bg_from_url(config.background_link)

placeholder = st.empty()
st.markdown("<h1 style='text-align: center; color: black;'>DoggoCare</h1>", unsafe_allow_html=True)
if config.profiles_dict[config.current_profile]['disable_back_next']:
    if placeholder.button("Back to main page"):
        st.switch_page("pages/page4.py")

st.markdown("<h4 style='text-align: center; color: black;'>Upload a picture of your dog:</h1>", unsafe_allow_html=True)

my_grid = grid(1, [1,2,1], [1, 5, 1], vertical_align="bottom")

# Row 1
uploaded_file = my_grid.file_uploader("dog-image", label_visibility='hidden')

# Row 2
my_grid.markdown("")
placeholder = my_grid.empty()
my_grid.markdown("")

if uploaded_file is not None:
    image_with_border = add_border(uploaded_file, border=10, color='black')
    config.profiles_dict[config.current_profile]['image'] = image_with_border
    placeholder.image(image_with_border, width=300)

if not config.profiles_dict[config.current_profile]['disable_back_next']:
    if my_grid.button("Back"):
        st.switch_page("pages/page2.py")

    my_grid.markdown("")

    if my_grid.button("Next"):
        st.switch_page("pages/page4.py")



import streamlit as st
from streamlit_extras.grid import grid
import datetime as dt
import config
from datetime import datetime

config.local_css("style.css")
config.add_bg_from_url(config.background_link)

placeholder = st.empty()
st.markdown("<h1 style='text-align: center; color: black;'>DoggoCare</h1>", unsafe_allow_html=True)
if config.profiles_dict[config.current_profile]['disable_back_next']:
    if placeholder.button("Back to main page"):
        st.switch_page("pages/page4.py")

st.markdown("<h4 style='text-align: center; color: black;'>Choose what would you like to be reminded of:</h1>", unsafe_allow_html=True)

my_grid = grid([1,3,1],
               [1,3,1], #1
               [1.4,1,1,1,1,1], #2
               [1, 3, 1], #3
               [1.4,1,1,1,1,1], #4
               [1,3,1], #5
               [1.1, 3, 1], #6
               [1.1,1,1,1,1], #7
               [1,3,1], #8
               [0.7,0.3,0.5,1,0.75], #9 # every
               [1,3,1], #10 # choose the last time
               [1,3,1], #11 # calender
               1, #12
               [1,4,1], #13
               vertical_align="bottom")

# E-Mail address
my_grid.markdown("")
config.email = my_grid.text_input('Enter your email for getting reminders:')
my_grid.markdown("")

# Row 1
my_grid.markdown("")
checked_feeding = my_grid.checkbox('Feeding your dog')
my_grid.markdown("")

# Row 2
my_grid.markdown("")
placeholder2_0 = my_grid.empty() # for selecting frequency
placeholder2_1 = my_grid.empty() # for first feeding
placeholder2_2 = my_grid.empty() # for second feeding
placeholder2_3 = my_grid.empty() # for third feeding
placeholder2_4 = my_grid.empty() # for fourth feeding

time_intervals = [str(dt.timedelta(minutes=30 * i))[:-3] for i in range(48)]

if checked_feeding:
    feeding_freq = placeholder2_0.selectbox("Frequency:", list(range(1,5)), key="feeding_freq")
    feeding_freq = int(feeding_freq)
    res = placeholder2_1.selectbox("First:", time_intervals, key="feeding_first")
    fixed_date = datetime.strptime('1900-01-01 ' + res, '%Y-%m-%d %H:%M')
    config.profiles_dict[config.current_profile]['feeding'][1] = fixed_date.time()
    for i in range(2, feeding_freq+1):
        if i == 2:
            res = placeholder2_2.selectbox("Second:", time_intervals, key="feeding_second")
        elif i == 3:
            res = placeholder2_3.selectbox("Third:", time_intervals, key="feeding_third")
        elif i == 4:
            res = placeholder2_4.selectbox("Fourth:", time_intervals, key="feeding_fourth")

        fixed_date = datetime.strptime('1900-01-01 ' + res, '%Y-%m-%d %H:%M')
        config.profiles_dict[config.current_profile]['feeding'][i] = fixed_date.time()
else:
    config.profiles_dict[config.current_profile]['feeding'] = {}
# Row 3
my_grid.markdown("")
checked_walking = my_grid.checkbox('Walking your dog')
my_grid.markdown("")

# Row 4
my_grid.markdown("")
placeholder4_0 = my_grid.empty() # for selecting frequency
placeholder4_1 = my_grid.empty() # for first walking
placeholder4_2 = my_grid.empty() # for second walking
placeholder4_3 = my_grid.empty() # for third walking
placeholder4_4 = my_grid.empty() # for fourth walking

time_intervals = [str(dt.timedelta(minutes=30 * i))[:-3] for i in range(48)]

if checked_walking:
    walking_freq = placeholder4_0.selectbox("Frequency:", list(range(1,5)), key="walking_freq")
    walking_freq = int(walking_freq)
    res = placeholder4_1.selectbox("First:", time_intervals, key="walking_first")
    fixed_date = datetime.strptime('1900-01-01 ' + res, '%Y-%m-%d %H:%M')
    config.profiles_dict[config.current_profile]['walking'][1] = fixed_date.time()
    for i in range(2, walking_freq+1):
        if i == 2:
            res = placeholder4_2.selectbox("Second:", time_intervals, key="walking_second")
        elif i == 3:
            res = placeholder4_3.selectbox("Third:", time_intervals, key="walking_third")
        elif i == 4:
            res = placeholder4_4.selectbox("Fourth:", time_intervals, key="walking_fourth")
        fixed_date = datetime.strptime('1900-01-01 ' + res, '%Y-%m-%d %H:%M')
        config.profiles_dict[config.current_profile]['walking'][i] = fixed_date.time()
else:
    config.profiles_dict[config.current_profile]['walking'] = {}

# Row 5
my_grid.markdown("")
checked_vaccinations = my_grid.checkbox('Getting vaccinations')
my_grid.markdown("")

# Row 6
placeholder6_0 = my_grid.empty()
placeholder6_1 = my_grid.empty()
placeholder6_2 = my_grid.empty()

# Row 7
# Define placeholders
my_grid.markdown("")
placeholder7_0 = my_grid.empty()
placeholder7_1 = my_grid.empty()
placeholder7_2 = my_grid.empty()
my_grid.markdown("")


if checked_vaccinations:
    placeholder6_0.markdown('')
    placeholder6_1.markdown(f"Choose the last time {config.current_profile} got vaccinated:")
    placeholder6_2.markdown('')

    config.profiles_dict[config.current_profile]['last_rabis'] = placeholder7_0.date_input('Rabies', format='DD/MM/YYYY', value=None, max_value=datetime.today().date())
    config.profiles_dict[config.current_profile]['last_hexagon'] = placeholder7_1.date_input('Hexagon', format='DD/MM/YYYY', value=None, max_value=datetime.today().date())
    config.profiles_dict[config.current_profile]['last_spirocerca'] = placeholder7_2.date_input('Spirocerca', format='DD/MM/YYYY', value=None, max_value=datetime.today().date())

else:
    config.profiles_dict[config.current_profile]['last_rabis'] = None
    config.profiles_dict[config.current_profile]['last_hexagon'] = None
    config.profiles_dict[config.current_profile]['last_spirocerca'] = None
# Row 6
my_grid.markdown("")
checked_haircut = my_grid.checkbox('Getting a haircut')
my_grid.markdown("")

# Row 8
my_grid.markdown("")
placeholder8_0 = my_grid.empty()
placeholder8_1 = my_grid.empty()
placeholder8_2 = my_grid.empty()
my_grid.markdown("")

# Save place for Row 9
placeholder9_0 = my_grid.empty()
placeholder9_1 = my_grid.empty()
placeholder9_2 = my_grid.empty()

# Save place for Row 10
placeholder10_0 = my_grid.empty()
placeholder10_1 = my_grid.empty()
placeholder10_2 = my_grid.empty()

if checked_haircut:
    placeholder8_0.write("Every")
    config.profiles_dict[config.current_profile]['haircut']["freq"] = int(placeholder8_1.selectbox("freq_haircut", list(range(1,13)), label_visibility="hidden"))
    config.profiles_dict[config.current_profile]['haircut']["interval"] = placeholder8_2.selectbox("time_haircut", ["weeks", "months"], label_visibility="hidden")

    # Row 9
    placeholder9_0.markdown('')
    placeholder9_1.markdown(f"Choose the last time {config.current_profile} got a haircut:")
    placeholder9_2.markdown('')

    # Row 10
    placeholder10_0.markdown('')
    config.profiles_dict[config.current_profile]['last_haircut'] = placeholder10_1.date_input('last_haircut', label_visibility='hidden', format="DD/MM/YYYY",
                                                    value=None, max_value=datetime.today().date())
    placeholder10_2.markdown('')
else:
    config.profiles_dict[config.current_profile]['last_haircut'] = None

# Row 11
my_grid.markdown("")


if not config.profiles_dict[config.current_profile]['disable_back_next']:
    # Row 12
    if my_grid.button("Back"):
        st.switch_page("pages/detailsPage.py")

    my_grid.markdown("")

    if my_grid.button("Next"):
        st.switch_page("pages/imagePage.py")


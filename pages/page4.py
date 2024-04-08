import streamlit as st
from streamlit_extras.grid import grid
import config
from datetime import datetime, timedelta
import calendar
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config.local_css("style.css")
config.add_bg_from_url(config.background_link)

current_date = datetime.now().date()
current_time = datetime.now().time()

config.profiles_dict[config.current_profile]['disable_back_next'] = True


def send_reminder(content):
    sender_email = "doggocare12@gmail.com"
    password = 'dixc odmd lxfc zqcf'
    recipient_email = config.email
    subject = "You have a new reminder from DoggoCare!"
    body = content

    try:
        # Create the email
        email = MIMEMultipart()
        email['From'] = sender_email
        email['To'] = recipient_email
        email['Subject'] = subject
        email.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, email.as_string())
            server.quit()
    except Exception as e:
        print("")


def time_diff(time1, time2):
    seconds1 = time1.hour * 3600 + time1.minute * 60 + time1.second
    seconds2 = time2.hour * 3600 + time2.minute * 60 + time2.second
    diff_seconds = abs(seconds2 - seconds1)
    hours, remainder = divmod(diff_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return hours, minutes

def user_output(action, reminder_time):
    hours, minutes = time_diff(current_time, reminder_time)
    name = config.current_profile
    hours_str = 'hours'
    minutes_str = 'minutes'
    if hours == 1:
        hours_str = 'hour'
    if minutes_str == 1:
        minutes_str = 'minute'

    if hours == 0 and minutes == 0:
        output = f"{action} {name} now"
    elif hours == 0:
        output = f"{action} {name} in {minutes} {minutes_str}"
    elif minutes == 0:
        output = f"{action} {name} in {hours} {hours_str}"
    else:
        output = f"{action} {name} in {hours} {hours_str} and {minutes} {minutes_str}"
    return output


def is_leap_year(year):
    # Returns True if the year is a leap year, False otherwise
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_difference(dt1, dt2):
    monthDays = [31, 28, 31, 30, 31, 30,
                 31, 31, 30, 31, 30, 31]

    n1 = dt1.year * 365 + dt1.day

    for i in range(0, dt1.month - 1):
        n1 += monthDays[i]

    n1 += sum(is_leap_year(year) for year in range(1, dt1.year))

    n2 = dt2.year * 365 + dt2.day
    for i in range(0, dt2.month - 1):
        n2 += monthDays[i]
    n2 += sum(is_leap_year(year) for year in range(1, dt2.year))

    return n2 - n1



def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return source_date.replace(year=year, month=month, day=day)

def get_next_date(freq_dict, last_occurrence):
    next_date = None
    freq = freq_dict.get("freq")
    interval = freq_dict.get("interval")
    if freq is not None and interval is not None:
        if interval == "weeks":
            next_date = last_occurrence + timedelta(weeks=freq)
        elif interval == "months":
            next_date = add_months(last_occurrence, freq)
    return next_date

grid_buttons = grid([0.2,1.5,1.5,1.3,1.5,1,0.5])
grid_buttons.markdown('')
if grid_buttons.button("Edit dog's details"):
    st.switch_page("pages/detailsPage.py")
if grid_buttons.button('Edit reminders'):
    st.switch_page("pages/page2.py")
if grid_buttons.button('Edit picture'):
    st.switch_page("pages/imagePage.py")
if grid_buttons.button("Dogs' profiles"):
    st.switch_page("pages/profiles.py")
if config.profiles_dict[config.current_profile]['image'] is not None:
    grid_buttons.image(config.profiles_dict[config.current_profile]['image'], width=100)
grid_buttons.markdown('')

st.markdown("<h1 style='text-align: center; color: black;'>DoggoCare</h1>", unsafe_allow_html=True)

my_grid = grid([2,4,1], #1
               [1.6,2,1], #2
               [2,3,1], #3
               [1,2,1], #4
               [1,2,1], #5
               [1,2,1], #6
               [1,2,1], #7
               [1,2,1], #8
               [1,2,1], #9
               vertical_align="bottom")

# Row 1
my_grid.markdown('')
if my_grid.button("Start a conversation with our DoggoBot!"):
    st.switch_page("pages/DoggoBot.py")
my_grid.markdown('')

# Row 2
my_grid.markdown('')
if my_grid.button("Find out your dog's mood!"):
    st.switch_page("pages/dogMood.py")
my_grid.markdown('')

# Row 3
my_grid.markdown('')
my_grid.markdown("<h3 style=color: black;'>Upcoming Events:</h3>", unsafe_allow_html=True)
my_grid.markdown('')

# Row 4
my_grid.markdown('')
placeholder1 = my_grid.empty()

for key, value in config.profiles_dict[config.current_profile]['walking'].items():
    if value > current_time:
        output = user_output('Walk', value)
        checked_walk = placeholder1.checkbox(output)
        if checked_walk:
            placeholder1.empty()
            config.profiles_dict[config.current_profile]['walking'].pop(key)
        break

my_grid.markdown('')

# Row 5
my_grid.markdown('')
placeholder2 = my_grid.empty()

for key, value in config.profiles_dict[config.current_profile]['feeding'].items():
    if value > current_time:
        output = user_output('Feed', value)
        checked_feed = placeholder2.checkbox(output)
        if checked_feed:
            placeholder2.empty()
            config.profiles_dict[config.current_profile]['feeding'].pop(key)
        break
my_grid.markdown('')

# Row 6
my_grid.markdown('')
placeholder3 = my_grid.empty()
if config.profiles_dict[config.current_profile]['last_haircut'] is not None:
    next_haircut_date = get_next_date(config.profiles_dict[config.current_profile]['haircut'], config.profiles_dict[config.current_profile]['last_haircut'])
    if next_haircut_date:
        days = get_difference(current_date, next_haircut_date)
        if 0 < days <= 7:
            checked_haircut = placeholder3.checkbox(f"Take {config.current_profile} to get a haircut in {days} days")
            if checked_haircut:
                placeholder3.empty()
                config.profiles_dict[config.current_profile]['last_haircut'] = next_haircut_date
        if days == 1:
            send_reminder(f"Take {config.current_profile} to get a haircut tomorrow!")

my_grid.markdown('')

# Row 7
my_grid.markdown('')
placeholder4 = my_grid.empty()
if config.profiles_dict[config.current_profile]['last_rabis'] is not None:
    next_rabis_date = get_next_date(config.rabis_dict, config.profiles_dict[config.current_profile]['last_rabis'])
    if next_rabis_date:
        days = get_difference(current_date, next_rabis_date)
        if 0 < days <= 7:
            checked_rabis = placeholder4.checkbox(f"Take {config.current_profile} to get a rabis vaccination in {days} days")
            if checked_rabis:
                placeholder4.empty()
                config.profiles_dict[config.current_profile]['last_rabis'] = next_rabis_date
        if days == 1:
            send_reminder(f"Take {config.current_profile} to get a rabis vaccination tomorrow!")
my_grid.markdown('')

# Row 8
my_grid.markdown('')
placeholder5 = my_grid.empty()
if config.profiles_dict[config.current_profile]['last_hexagon'] is not None:
    next_hexagon_date = get_next_date(config.hexagon_dict, config.profiles_dict[config.current_profile]['last_hexagon'])
    if next_hexagon_date:
        days = get_difference(current_date, next_hexagon_date)
        if 0 < days <= 7:
            checked_hexagon = placeholder5.checkbox(f"Take {config.current_profile} to get a hexagon vaccination in {days} days")
            if checked_hexagon:
                placeholder5.empty()
                config.profiles_dict[config.current_profile]['last_hexagon'] = next_hexagon_date
        if days == 1:
            send_reminder(f"Take {config.current_profile} to get a hexagon vaccination tomorrow!")
my_grid.markdown('')

# Row 9
my_grid.markdown('')
placeholder6 = my_grid.empty()
if config.profiles_dict[config.current_profile]['last_spirocerca'] is not None:
    next_spirocerca_date = get_next_date(config.spirocerca_dict, config.profiles_dict[config.current_profile]['last_spirocerca'])
    if next_spirocerca_date:
        days = get_difference(current_date, next_spirocerca_date)
        if 0 < days <= 7:
            checked_spirocerca = placeholder6.checkbox(f"Take {config.current_profile} to get a spirocerca vaccination in {days} days")
            if checked_spirocerca:
                placeholder6.empty()
                config.profiles_dict[config.current_profile]['last_spirocerca'] = next_spirocerca_date
        if days == 1:
            send_reminder(f"Take {config.current_profile} to get a spirocerca vaccination tomorrow!")
my_grid.markdown('')
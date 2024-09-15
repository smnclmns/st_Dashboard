# Description: This module contains functions to extract events from ICS-URLs and create a timeline widget for Streamlit.

# Imported Moduls:
import streamlit as st # For Streamlit-Caching
import requests # For HTTP-Requests
import pytz # For Timezone-Handling
import pandas as pd # For Data-Handling

from ics import Calendar # For ICS-Handling
from datetime import datetime # For Date-Handling
from jinja2 import Template # For HTML-Template-Rendering

# imported functions
from time import sleep # For time delays (stabilizing due to network issues)

# Three main functions: get_timeline_options, get_groups_from_members_df, get_tamam_member_calender_events

def get_timeline_options(**kwargs) -> dict:
    '''
    Returns a dictionary with the options for the timeline widget.
    The options are:
    - max: The maximum date for the timeline
    - min: The minimum date for the timeline
    - locale: The locale for the timeline

    The options can be customized by passing keyword arguments.
    The following keyword arguments are supported:
    - months_ahead: The number of months ahead for the maximum date
    ... and more to come
    
    '''

    # Get current date and define time range for the timeline
    current_date = f"{datetime.now().isoformat()}"

    if "months_ahead" in kwargs: # Number of months ahead
        # Convert months to number of years and months (e.g. 13 months -> 1 year and 1 month)
        months_ahead = int(kwargs["months_ahead"])
        year_ahead = months_ahead // 12
        months_ahead = months_ahead % 12
        # Calculate the maximum date
        replace_month = datetime.now().month + months_ahead
        if replace_month > 12:
            replace_month = replace_month % 12
            year_ahead += 1
        replace_year = datetime.now().year + year_ahead
        max_date = f"{datetime.now().replace(year=replace_year, month=replace_month).isoformat()}"
    else:
        max_date = f"{datetime.now().replace(year=datetime.now().year+1).isoformat()}"     
        
    options = {
        'max': max_date,
        'min': current_date,
        'locale': 'de',
    }
    return options

@st.cache_data(ttl=3600) # Cache for 1 hour
def get_groups_from_members_df(members_df: pd.DataFrame) -> list[dict]:
    '''
    Returns a list of dictionaries with the group information for the timeline widget.
    The group information is:
    - id: The id of the group
    - content: The content of the group
    - title: The title of the group
    
    The group information is extracted from the members dataframe.
    
    '''

    groups = []
    for name in members_df["Name"].values:
        firstname = name.split(" ")[0]
        groups.append({
            'id': firstname,
            'content': firstname,
            'title': firstname,
        })
    return groups

@st.cache_data(ttl=3600) # Cache for 1 hour
def get_tamam_member_calender_events(members_df: pd.DataFrame) -> list[dict]:
    '''
    Returns a list of dictionaries with the event information for the timeline widget.
    The event information is:
    - id: The id of the event
    - content: The content of the event
    - start: The start date and time of the event
    - end: The end date and time of the event
    - group: The group of the event
    - title: The title of the event
    - style: The style of the event

    The event information is extracted from the members dataframe.

    '''

    events = []
    for name, url in members_df[["Name", "ICS_URL"]].values:
        cal = get_calender_from_url(url)
        if cal is None:
            continue
        events.extend(_extract_calender_events(name, cal))
    return events


# -- Helper functions --

def get_calender_from_url(url: str) -> Calendar:
    '''
    Returns a Calendar object from the given URL.
    The URL should be a string.
    If the URL is not a string, the function returns None.
    If the URL is not valid, the function raises an exception.
    If the URL is valid, the function returns a Calendar object.

    '''

    if not isinstance(url, str):
        return None
    
    ics_response = requests.get(url)
    ics_response.raise_for_status()

    for attempts in range(3):        

        try:
            cal = Calendar(ics_response.text)
        except Exception as e:
            print(f"Error: {e}")
            sleep(0.5)
            continue
    return cal

def _get_name_html(member: str, event_name: str) -> str:
    with open("custom_moduls/calender_widget/name_template.html", "r") as f:
        template = Template(f.read())
    return template.render(member=member, event_name=event_name)

def _get_title_html(event_name: str, member: str, start: str, end: str, location: str, des: str) -> str:
    with open("custom_moduls/calender_widget/title_template.html", "r") as f:
        template = Template(f.read())

    start_date, start_time = start.split("T")
    _, end_time = end.split("T")

    weekday = datetime.fromisoformat(start).strftime("%A")
    start_date = f"{weekday}, {start_date}"

    if des and len(des) > 25:
        des = des[:25] + "..."

    return template.render(
        event_name=event_name,
        member=member,
        start_date=start_date,
        start_time=start_time[:5],
        end_time=end_time[:5],
        location=location or "No Location",
        description=des or "No Description",
        )

def _extract_calender_events(member: str, cal: Calendar) -> list[dict]:
    '''
    Returns a list of dictionaries with the event information for the timeline widget.
    The event information is:
    - id: The id of the event
    - content: The content of the event
    - start: The start date and time of the event
    - end: The end date and time of the event
    - group: The group of the event
    - title: The title of the event
    - style: The style of the event
    
    The event information is extracted from the calendar object.
    
    '''

    local_tz = pytz.timezone('Europe/Berlin')

    events = []
    for i, event in enumerate(cal.events):

        # Skip events that are already over
        if event.end.astimezone(local_tz).date() < datetime.now().date():
            continue

        # Skip events that are generated by Reclaim.ai
        if event.description and "Reclaim" in event.description:
            continue

        
        # Shift time by 2 hours -> GMT+2
        event.end = event.end.astimezone(local_tz)
        event.begin = event.begin.astimezone(local_tz)     

        # Convert Arrow-Objects in ISO 8601-Strings
        start = event.begin.isoformat()
        end = event.end.isoformat()

        # Create HTML-Content und Title
        content = _get_name_html(member, event.name)
        title = _get_title_html(event.name, member, start, end, event.location, event.description)

        # Set Style
        style = ""

        if event.description:
            if event.description == "Tamam":
                style += "border-color: gold; background-color: gold;"
        else:
            style += "border-color: grey; background-color: grey;"
        
        # Append Event-dict to List
        events.append({
            'id': f"{member}_{i}",
            'content': content,
            'start': start,
            'end': end,
            'group': member.split(' ')[0],
            'title': title,
            'style': style,
        })
    return events
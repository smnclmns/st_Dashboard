"""
Description: This module contains functions to extract events from ICS-URLs and create a timeline widget for Streamlit.

"""

# Imported Moduls:
import streamlit as st # For Streamlit-Caching
import pandas as pd # For Data-Handling
from datetime import datetime # For Date-Handling

# imported functions
from time import sleep # For time delays (stabilizing due to network issues)
from services.calender_widget.streamlit_timeline import st_timeline # For the timeline widget
from services.calender_widget.helper_functions import (
    get_calender_from_url,
    extract_calender_events,
    months_ahead,
    months_behind,)

# Three main functions: get_timeline_options, get_groups_from_members_df, get_tamam_member_calender_events

def get_timeline_options(**kwargs) -> dict:
    '''
    Returns a dictionary with the options for the timeline widget.
    The options are:
    - max: The maximum date for the timeline
    - min: The minimum date for the timeline
    - locale: The locale for the timeline
    - height: The height of the timeline

    The options can be customized by passing keyword arguments.
    The following keyword arguments are supported:
    - months_ahead: The number of months ahead for the maximum date
    - months_behind: The number of months behind for the minimum date
    - height: The height of the timeline
    ... and more to come
    
    '''
    
    def update_options(options: dict, **kwargs) -> dict:
        for key, value in kwargs.items():
            if key == "months_ahead" or key == "months_behind":
                continue
            if key not in options:
                options[key] = value
        return options

    if "months_ahead" in kwargs: 
        max_date = months_ahead(int(kwargs["months_ahead"]))
    else:
        max_date = f"{datetime.now().replace(year=datetime.now().year+1).isoformat()}"

    if "months_behind" in kwargs:
        min_date = months_behind(int(kwargs["months_behind"]))
    else:
        min_date = f"{datetime.now().isoformat()}"
        
    options = {
        'max': max_date,
        'min': min_date,
        'locale': 'de',
    }

    options = update_options(options, **kwargs)
        
    return options

@st.cache_data(ttl=3600) # Cache for 1 hour
def get_groups_from_members_df() -> list[dict]:
    '''
    Returns a list of dictionaries with the group information for the timeline widget.
    The group information is:
    - id: The id of the group
    - content: The content of the group
    - title: The title of the group
    
    The group information is extracted from the members dataframe.
    
    '''

    members_df: pd.DataFrame = st.session_state.ch.members_df

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
def get_tamam_member_calender_events() -> list[dict]:
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

    members_df: pd.DataFrame = st.session_state.ch.members_df

    events = []
    for name, url in members_df[["Name", "ICS_URL"]].values:
        cal = get_calender_from_url(url)
        if cal is None:
            continue
        events.extend(extract_calender_events(name, cal))
    
    return events

def timeline(
        options: dict,
        items: list[dict] = get_tamam_member_calender_events(),
        groups: list[dict] = get_groups_from_members_df(),
        ) -> None:    
    '''
    Displays a timeline widget in Streamlit.
    Args:
        options: A dictionary with the options for the timeline widget
        items: A list of dictionaries with the event information for the timeline widget
        groups: A list of dictionaries with the group information for the timeline widget

    '''

    st_timeline(
        items=items,
        groups=groups,
        options=options,
    )


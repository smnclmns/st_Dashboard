import requests
from ics import Calendar
import pandas as pd
from datetime import datetime

def get_timeline_options():
    current_date = f"{datetime.now().isoformat()}"
    one_year_ago = f"{datetime.now().replace(year=datetime.now().year-1).isoformat()}"
    five_years_later = f"{datetime.now().replace(year=datetime.now().year+5).isoformat()}"
    options = {
        'max': five_years_later,
        'min': one_year_ago,
        'locale': 'de',
    }
    return options

def get_groups_from_members_df(members_df: pd.DataFrame) -> list[dict]:
    groups = []
    for name in members_df["Name"].values:
        firstname = name.split(" ")[0]
        groups.append({
            'id': firstname,
            'content': firstname,
            'title': firstname,
        })
    return groups

def get_tamam_member_calender_events(members_df: pd.DataFrame) -> list[dict]:

    events = []
    for name, url in members_df[["Name", "ICS_URL"]].values:
        cal = get_calender_from_url(url)
        if cal is None:
            continue
        events.extend(_extract_calender_events(name, cal))
    return events

def get_calender_from_url(url: str) -> Calendar:

    if not isinstance(url, str):
        return None
    
    ics_response = requests.get(url)
    ics_response.raise_for_status()
    return Calendar(ics_response.text)

def _get_name_html(member: str, event_name: str) -> str:
    html_tag = f'''
    <div style="
    width: 100%;
    font-family: Arial, sans-serif;">
        <div style="font-size: 9px; font-weight: bold; color: #555; margin-bottom: 5px; text-align: left;">
            {member}
        </div>
        <div style="font-size: 12px; font-weight: normal; color: #000; text-align: center;">
            {event_name}
        </div>
    </div>
    '''
    return html_tag

def get_title_html(event_name: str, member: str, start: str, end: str, location: str) -> str:
    html_tag = f'''
    <div style="
    border: 1px solid #ccc;
    padding: 10px;
    width: 100%;
    font-family: Arial, sans-serif;">
        <div style="font-size: 9px; font-weight: bold; color: #555; margin-bottom: 5px; text-align: left;">
            {member}
        </div>
        <div style="font-size: 12px; font-weight: normal; color: #000; text-align: center;">
            {event_name}
        </div>
        <div style="font-size: 9px; font-weight: normal; color: #555; text-align: left;">
            {start.split("T")[0]}: {start.split("T")[1][:5]} - {end.split("T")[1][:5]}
        </div>
        <div style="font-size: 9px; font-weight: normal; color: #555; text-align: left;">
            {location if location else "No location"}
        </div>
    </div>
    '''
    return html_tag


def _extract_calender_events(member: str, cal: Calendar) -> list[dict]:
    events = []
    for i, event in enumerate(cal.events):
        
        # Shift time by 2 hours -> GMT+2
        event.end = event.end.shift(hours=2)
        event.begin = event.begin.shift(hours=2)

        # Convert Arrow-Objects in ISO 8601-Strings
        start = event.begin.isoformat()
        end = event.end.isoformat()
        content = _get_name_html(member, event.name)
        title = get_title_html(event.name, member, start, end, event.location)

        style = ""

        if event.description:
            if event.description == "Tamam":
                style += "border-color: gold; background-color: gold;"
            elif "Reclaim" in event.description:
                style += "border-color: green; background-color: green;"
        else:
            style += "border-color: grey; background-color: grey;"
        
        events.append({
            'id': i,
            'content': content,
            'start': start,
            'end': end,
            'group': member.split(' ')[0],
            'title': title,
            'style': style,
        })
    return events
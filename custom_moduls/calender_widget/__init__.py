import json

def get_calender_options() -> dict:
    with open("custom_moduls/calender_widget/calender_options.json", "r") as f:        
        return json.load(f)
    
def get_calender_events() -> dict:
    # TODO: Implement a way to get the events from the members calenders
    with open("custom_moduls/calender_widget/calender_events.json", "r") as f:
        return json.load(f)
    
def get_custom_css() -> str:
    with open("custom_moduls/calender_widget/custom.css", "r") as f:
        return f.read()
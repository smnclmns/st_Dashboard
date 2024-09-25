import json
import os
import streamlit as st
import streamlit.components.v1 as components

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
_component_func = components.declare_component(
    "st_timeline", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def st_timeline(
    items, groups=None, options=None, style=None, width="100%", height="200px", key=None
):
    """Create a vis.js timeline with bidirectional communication. For more information about vis.js timeline, please visit https://visjs.github.io/vis-timeline/docs/timeline/.

    Args:
        items (list): A list of timeline items.
        groups (list, optional): A list of timeline groups. Defaults to None.
        options (dict, optional): A dictionary of timeline options. Defaults to None.
        style (str, optional): A string of css styles or a path to a css file. Defaults to None.
        width (str, optional): The width of the timeline. Defaults to "100%".
        height (str, optional): The height of the timeline. Defaults to "200px".
        key (str, optional): A unique key for the timeline. Defaults to None.

    Returns:
        streamlit component: A vis.js timeline.
    """

    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.

    if not isinstance(options, dict):
        raise TypeError("options must be a dictionary")

    if "width" not in options:
        options["width"] = width
    if "height" not in options:
        options["height"] = height

    for index, item in enumerate(items):
        if "id" not in item:
            item["id"] = index

    options_json = json.dumps(options)
    items_json = json.dumps(items)
    groups_json = json.dumps(groups)

    component_value = _component_func(
        items=items_json, groups=groups_json, options=options_json, key=key
    )

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.

    if component_value is None:
        return None
    else:
        for item in items:
            if item["id"] == component_value:
                return item
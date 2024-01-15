import streamlit as st
import toml
import datetime
import pandas
from streamlit_tags import st_tags

# Load the logbook TOML file
try:
    with open("logbook.toml", "r") as f:
        log_data = toml.load(f)
except FileNotFoundError:
    log_data = {"entries": []}
if len(log_data)<0:
    log_data = {"entries": []}


# Display the existing log entries
st.title("Experiment Logbook")

def update_toml():
    with open("logbook.toml", "w") as f:
        toml.dump(log_data, f)
        
def update_log_data():
    L = len(log_data["entries"])
    edited_rows = st.session_state["edited_data"]["edited_rows"]
    for row in edited_rows:
        if "timestamp" in edited_rows[row]:
            edited_rows[row]["timestamp"] = datetime.datetime.fromisoformat(edited_rows[row]["timestamp"])
            

        log_data["entries"][L-int(row)].update(edited_rows)
    del st.session_state["edited_data"]
    update_toml()

# Form to add a new entry
with st.form("add_entry"):
    log_text = st.text_area("Log Text")
    tags = st_tags(label="Tags",
                                    text='Press enter to add more',
                                    suggestions=["experiment", "observation", "analysis", "other"])

    submit = st.form_submit_button("Add Entry")

        

    if submit:  # Check if the form was submitted
        timestamp = datetime.datetime.now().isoformat(timespec="seconds")
        new_entry = {
            "id": max([0]+[entry["id"] for entry in log_data["entries"]])+1,
            "timestamp": timestamp,
            "text": log_text,
            "tags": tags,
        }
        log_data["entries"].append(new_entry)
        update_toml()
        
toggle_delete = st.toggle("edit logbook")

entries = {index:pandas.Series(entry) for index,entry in enumerate(log_data["entries"][::-1])}
data = pandas.DataFrame(entries).T
if len(data):
    data["timestamp"] = pandas.to_datetime(data["timestamp"])
    data = data.set_index("id")
if toggle_delete:
    data = st.data_editor(data,use_container_width=True,num_rows= "dynamic",key="edited_data",column_order=["timestamp","text","tags"],hide_index=True)
else:
    data = st.data_editor(data,use_container_width=True,key="edited_data",column_order=["timestamp","text","tags"],hide_index=True)

st.write(st.session_state["edited_data"])
update_log_data()
st.write(log_data)



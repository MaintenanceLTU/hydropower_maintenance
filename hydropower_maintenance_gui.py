import tkinter as tk
import json
# import pandas as pd
# import numpy as np
import re

def save_json():
    # Read the JSON file
    with open('hydropower_maintenance.json', 'r') as file:
        data = json.load(file)

    # Update the data with the input values
    component = component_entry.get()
    item_type = type_entry.get()
    action = action_entry.get()
    failure_frequency = float(failure_frequency_entry.get())
    admin_delay_min = float(admin_delay_min_entry.get())
    admin_delay_max = float(admin_delay_max_entry.get())
    repair_time_min = float(repair_time_min_entry.get())
    repair_time_max = float(repair_time_max_entry.get())

    # Create a new item
    new_item = {
        "component": component,
        "type": item_type,
        "action": action,
        "failure_frequency": failure_frequency,
        "admin_delay": [admin_delay_min, admin_delay_max],
        "repair_time": [repair_time_min, repair_time_max]
    }

    # Add the new item to the JSON data
    if component in data:
        data[component].append(new_item)
    else:
        data[component] = [new_item]

    # Save the updated JSON data to the file
    with open('hydropower_maintenance.json', 'w') as file:
        json.dump(data, file, indent=4)

    print("JSON file saved.")

def load_json():
    # Read the JSON file
    with open('hydropower_maintenance.json', 'r') as file:
        data = json.load(file)

    # Get the filter values from the input fields
    # component = component_entry.get()
    # item_type = type_entry.get()
    # action = action_entry.get()
   
    
    # Filter the data based on the input values
    # df = pd.DataFrame(data)
    # mask = np.ones(df.shape[0], dtype=bool)
    # if component:
    #     print(component)
    #     mask = (mask) & (df['component'].str.contains(component, regex=True))
    # if item_type:
    #     print(item_type)
    #     mask = (mask) & (df['type'].str.contains(item_type, regex=True, case=False))
    # if action:
    #     print(action)
    #     mask = (mask) & (df['action'].str.contains(action, regex=True, case=False))
    
    # filtered_data = [dict(row.dropna()) for _,row in df[mask].iterrows()]

    # Get the filter values from the input fields
    component_pattern = component_entry.get() or ''
    type_pattern = type_entry.get() or ''
    action_pattern = action_entry.get() or ''    

    # Filter the data based on the input values
    filtered_data = []
    
    for item in data:
        if (re.search(component_pattern, item['component'], re.IGNORECASE) is None) or \
           (re.search(type_pattern, item['type'], re.IGNORECASE) is None) or \
           (re.search(action_pattern, item['action'], re.IGNORECASE) is None):
            continue
        filtered_data.append(item)
        
    # Clear the existing text in the output text box
    output_text.delete('1.0', tk.END)

    # Convert the filtered data to a formatted string and display it in the output text box
    formatted_data = json.dumps(filtered_data, indent=4)
    output_text.insert(tk.END, formatted_data)

# Create the main window
window = tk.Tk()

# Create input fields and labels for the JSON values
component_label = tk.Label(window, text="Component:")
component_entry = tk.Entry(window)

type_label = tk.Label(window, text="Type:")
type_entry = tk.Entry(window)

action_label = tk.Label(window, text="Action:")
action_entry = tk.Entry(window)

failure_frequency_label = tk.Label(window, text="Failure Frequency:")
failure_frequency_entry = tk.Entry(window)

admin_delay_min_label = tk.Label(window, text="Admin Delay Min:")
admin_delay_min_entry = tk.Entry(window)

admin_delay_max_label = tk.Label(window, text="Admin Delay Max:")
admin_delay_max_entry = tk.Entry(window)

repair_time_min_label = tk.Label(window, text="Repair Time Min:")
repair_time_min_entry = tk.Entry(window)

repair_time_max_label = tk.Label(window, text="Repair Time Max:")
repair_time_max_entry = tk.Entry(window)

save_button = tk.Button(window, text="Save", command=save_json)
load_button = tk.Button(window, text="Load", command=load_json)

output_text = tk.Text(window, height=10, width=50)

component_label.grid(row=0, column=0)
component_entry.grid(row=0, column=1)

type_label.grid(row=1, column=0)
type_entry.grid(row=1, column=1)

action_label.grid(row=2, column=0)
action_entry.grid(row=2, column=1)

failure_frequency_label.grid(row=3, column=0)
failure_frequency_entry.grid(row=3, column=1)

admin_delay_min_label.grid(row=4, column=0)
admin_delay_min_entry.grid(row=4, column=1)

admin_delay_max_label.grid(row=5, column=0)
admin_delay_max_entry.grid(row=5, column=1)

repair_time_min_label.grid(row=6, column=0)
repair_time_min_entry.grid(row=6, column=1)

repair_time_max_label.grid(row=7, column=0)
repair_time_max_entry.grid(row=7, column=1)

save_button.grid(row=8, column=0)
load_button.grid(row=8, column=1)

output_text.grid(row=9, columnspan=2)

window.mainloop()


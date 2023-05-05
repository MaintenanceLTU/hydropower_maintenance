import numpy as np
import datetime
import json

def generate_work_orders(start_date, end_date, maintenance_actions):
    work_orders = []
    current_date = start_date + datetime.timedelta(days=abs(np.random.normal(1, 1)))

    while current_date < end_date:
        # Generate maintenance work orders
        #for component in maintenance_actions:
        for action in maintenance_actions:
            component = action['component']
            action_type = action['type']
            action_description = action['action']
            if 'failure_frequency' in action:
                frequency = action['failure_frequency']
            else:
                frequency = action['frequency']
            admin_delay_params = action['admin_delay']
            repair_time_params = action['repair_time']

            if np.random.random() < frequency:
                admin_delay = np.random.lognormal(*admin_delay_params)
                repair_time = np.random.lognormal(*repair_time_params)

                admin_start_date = current_date + datetime.timedelta(days=admin_delay)
                admin_end_date = admin_start_date + datetime.timedelta(days=repair_time)

                work_order = {
                    "type": action_type,
                    "component": component,
                    "action": action_description,
                    "date_reported": current_date.strftime("%Y-%m-%d %H:%M"),
                    "date_started": admin_start_date.strftime("%Y-%m-%d %H:%M"),
                    "date_completed": admin_end_date.strftime("%Y-%m-%d %H:%M")
                }
                work_orders.append(work_order)

        current_date += datetime.timedelta(days=1)

    return work_orders

# Example usage
start_date = datetime.datetime(2000, 1, 1)
end_date = datetime.datetime(2020, 12, 31)

# Open the JSON file
with open('hydropower_maintenance.json') as file:
    # Parse the JSON data
    maintenance_data = json.load(file)

work_orders = generate_work_orders(start_date, end_date, maintenance_data)

# Write the JSON file
with open('hydropower_work_orders.json', 'w') as file:
    # Write the JSON data
    json.dump(work_orders, file, indent=4)

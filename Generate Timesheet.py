import csv
import os
import random
import pandasai.pandas as pd
from pandasai import Agent
from datetime import datetime, timedelta
from pandasai import SmartDataframe

# Define activity names, categories, resource names
activity_names = ['Activity A', 'Activity B', 'Activity C', 'Activity D', 'Activity E', 'Activity F', 'Activity G', 'Activity H', 'Activity I', 'Activity J']
activity_categories = {'Activity A': 'Category 1','Activity B': 'Category 1','Activity C': 'Category 2','Activity D': 'Category 2','Activity E': 'Category 3',
                       'Activity F': 'Category 3','Activity G': 'Category 4','Activity H': 'Category 4','Activity I': 'Category 5','Activity J': 'Category 5'}
resource_names = ['Resource 1', 'Resource 2', 'Resource 3', 'Resource 4', 'Resource 5', 'Resource 6', 'Resource 7', 'Resource 8']
# Define function to generate time logged randomly between 4 and 10 hours
def generate_time_logged():
    return random.randint(4, 10)

# Generate dates to cover all weeks of 2023
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 1, 1)  # Extend the end date to cover all weeks
dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days) if (start_date + timedelta(days=x)).isoweekday() == 1]

data = []

# Generate data
for date in dates:
    for resource in resource_names:
        total_hours = 0
        while total_hours < 35:
            activity_name = random.choice(activity_names)
            activity_category=activity_categories[activity_name]
            time_logged = generate_time_logged()
            total_hours += time_logged
            data.append([activity_name, activity_category,resource, date, time_logged])

# Create a DataFrame
timesheet = pd.DataFrame(data, columns=['Activity Name','Activity Category','Resource Name', 'Date of log', 'Time logged'])

#timesheet.to_csv('activity_log.csv')
print(timesheet)
API_KEY='$2a$10$5bkoLVv3gkrg7Q.Mg4EnAej5S7NXOrnJ2ajOwI.cvECMHvTzxl4iu'
os.environ['PANDASAI_API_KEY']=API_KEY
timesheet_=SmartDataframe(timesheet)


agent=Agent(timesheet_)
agent.chat('Number of total hours logged')


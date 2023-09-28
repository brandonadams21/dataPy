import pandas as pd
import plotly.express as px
import requests


## Firestore url for data
data_url = "https://firestore.googleapis.com/v1/projects/sat-saas/databases/(default)/documents/testCSJ/2023-05-17/SHOTS?pageSize=300"

## fetch all of the data
response = requests.get(data_url)

## Check if request is accepted
if response.status_code == 200:
    ## parse the response into json
    json_data = response.json()

    # For this to work, need to take the time value out of the firestore structure
    start_timestamps = [entry['fields']['start']['stringValue'] for entry in json_data['documents']]
    
    # Manually add the date to the chart. Will find a way to do this dynamically
    consistent_date = '2023-05-17'
    # add the date by the timestamp field
    start_timestamps = [consistent_date + ' ' + timestamp for timestamp in start_timestamps]
    
    # Need to convert the time from it's current format to a format that will be accepted for this package plotly
    start_timestamps = pd.to_datetime(start_timestamps, format='%Y-%m-%d %H:%M:%S', errors='coerce')

    # Create a DataFrame with the converted 'start' timestamps
    df = pd.DataFrame({'Time': start_timestamps})

    # Add the 'shotCount' column from the original JSON data
    df['Shot Count'] = [entry['fields']['shotCount']['stringValue'] for entry in json_data['documents']]

    # Create a scatter plot
    fig = px.scatter(df, y='Shot Count', x='Time', title='Firestore Data')

    # show the plot
    fig.show()
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

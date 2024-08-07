import os
import json
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest

# Property ID
PROPERTY_ID = "446474801"

# Path to your service account key file
KEY_FILE_CONTENT = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Initialize the Analytics Data API Client
def initialize_analyticsdata():
    credentials_info = json.loads(KEY_FILE_CONTENT)
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    client = BetaAnalyticsDataClient(credentials=credentials)
    return client

# Get a report from the Analytics Data API
def get_report(client):
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[{"name": "date"}],
        metrics=[{"name": "activeUsers"}, {"name": "averageSessionDuration"}],
        date_ranges=[{"start_date": "2024-01-01", "end_date": "2024-12-31"}]
    )
    response = client.run_report(request)
    return response

# Save the report data to a CSV file
def save_to_csv(response):
    data = []
    for row in response.rows:
        date = row.dimension_values[0].value
        active_users = row.metric_values[0].value
        avg_session_duration = row.metric_values[1].value
        data.append([date, active_users, avg_session_duration])

    df = pd.DataFrame(data, columns=["date", "activeUsers", "averageSessionDuration"])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')
    df.to_csv('analytics_data.csv', index=False)

# Main function
def main():
    print(f"Using PROPERTY_ID: {PROPERTY_ID}")
    client = initialize_analyticsdata()
    response = get_report(client)
    save_to_csv(response)
    print("Data fetched and saved to analytics_data.csv successfully.")

if __name__ == "__main__":
    main()

# Store Monitoring

This README provides an overview of the logic and functionality behind the Store Uptime/Downtime Calculator, which calculates the uptime and downtime for a all the store instances within specific time intervals. The calculator processes store logs and operating hours to generate accurate uptime and downtime metrics.

## Installation

1. Ensure you have Python 3.x and pip installed on your system.

2. Clone the Taskboard App repository to your local machine:
   ```shell
   git clone https://github.com/prathameshh27/StoreMonitoring.git
   ```

3. Navigate to the project directory:
   ```shell
   cd StoreMonitoring
   ```

4. Set up a virtual environment (optional but recommended) to isolate dependencies:
   ```shell
   python -m venv env
   source env/bin/activate   # On macOS/Linux
   env\Scripts\activate      # On Windows
   ```

5. Install the required packages using pip:
    ```shell
    pip install -r requirements.txt
    ```

6. Apply the database migrations:
    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Create a super user
    ```shell
    python manage.py createsuperuser
    ```

8. Unzip the database from the StoreMonitoring folder to use the data


## Report Generation APIs

Below are the API enpoints available for triggering and retrieving reports:

### Trigger Report Generation - `/trigger_report`

This API initiates the generation of a report from the stored data. It requires no input parameters and returns a unique `report_id` that can be used to poll the status of report completion.

**Input: None**

**Output:**
- `report_id` (Randomly generated string)
  
### Get Report Status or CSV - `/get_report`

This API is used to retrieve the status of the report generation or the generated CSV file.

**Input:**
- `report_id` (Report identifier obtained from the `/trigger_report` API)

**Output:**
- If report generation is still in progress, the API returns `"Running"` as the output.
- If report generation is complete, the API returns `"Complete"` along with the CSV file containing the specified schema.


## Debug Instructions

To debug the Store Monitoring App, follow these steps:

1. Start with the debugging URL provided to simulate the calculation process.
2. The process begins by calculating time intervals and identifying operating hours.
3. The valid intervals are used to analyze logs and calculate uptime/downtime.
4. The results are displayed per local timeframe for hourly, daily, and weekly intervals.

Feel free to adapt and integrate this logic into your project to accurately monitor store uptime and downtime.

For further assistance or questions, contact [your contact information].



## Debugging Endpoint

For debugging purposes, you can use the following endpoint:
- Debugging URL: [http://127.0.0.1:8000/api/debug_code/<store_id>](http://127.0.0.1:8000/api/debug_code/2311272071941344516)
- Eg: [http://127.0.0.1:8000/api/debug_code/2311272071941344516](http://127.0.0.1:8000/api/debug_code/2311272071941344516)
- This URL triggers the `debug_code` view, which is a starting point to simulate the calculations.
- The steps can be viewed in the console and can be related with the logic explained below.

## Logic Overview

### `debug_code` View

The `debug_code` view is responsible for initializing the calculation process. It sets the `max_date_utc` to the current time (UTC) and triggers the `get_store_report` function.

### `get_store_report` Function

This function handles a single store instance. It retrieves the uptime and downtime for specific time intervals (past hour, past day, past week). These intervals are calculated in UTC and passed to the `get_activity_in_mins` function.

### `get_activity_in_mins` Function

The `get_activity_in_mins` function accepts an interval and retrieves the uptime and downtime within the specified period. It collects necessary dependencies to compute the results:

- Store Timezone
- Store Operating Hours in the input range
- Store Logs
- Input Timeframe (provided as input to the function)
- Days (represented as a circular list for interval processing)

The function iterates over all the operating hours of the store and identifies the relevant operating intervals. It then checks for overlaps between operating hours and the input interval.
You will see this message before the loop starts - `Below are the Operating hours for the store:  2311272071941344516`

Let us relate this with the console logs:
At this point, We have the very 1st interval / operation hours in local time.
This is skipped due to detection of invalid interval. Function moves to next interval. 
The function gets the day and identifies the exact operating interval from the past which can be seen in the console as below:

`
Day of the week: 2
Local Interval:         2023-01-25 10:00:00-05:00               2023-01-25 23:59:59-05:00
UTC Interval:           2023-01-25 15:00:00+00:00               2023-01-26 04:59:59+00:00
`

Next the fuction checks the overlap between operating hours (OH) and input interval / timeframe (IP)

IPs1 ------------- IPe1
        OHs ------------- OHe
                 IPs2 ------------- IPe2

Where, 
IPs, IPe are Input start and end
OHs, OHe are Operating hours start and end

Consider 1st case,
max(IPs1, OHs) = OHs
min(IPe1, OHe) = IPe1

Hence the valid interval to check the uptime / downtime would be (OHs, IPe1)
You will see the below line on the console if a valid frame is found:
`Valid/applicable Interval:      2023-01-25 17:13:22.479220+00:00      2023-01-25 18:13:22.479220+00:00`


If valid intervals are found, the function calls `process_logs` to analyze the logs and calculate uptime/downtime. If no operating hours are found, a continuous 24/7 operational interval is considered.

### `process_logs` Function

The `process_logs` function analyzes logs within a valid interval to calculate possible uptime and downtime. 
Assumptions include:

- If no logs are found, the store is considered active.
- Downtime is identified when inactive logs are present.
- Inactive windows are calculated by finding the longest difference between inactive and active records.
- If the function identifies an inactive period within the timeframe, the period from the start to the inactive record is considered uptime, and the inactive record to the end is considered downtime.
        start |---------------InA-------| end
The output of this fuction would be the uptime / downtime in minutes per Valid frame:
`Local Timeframe - Uptime / Downtime:  60.0    0`

All the local calculations are combined together to calculate the final up/down time per hr, day, week.
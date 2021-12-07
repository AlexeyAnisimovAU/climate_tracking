# climate_tracking

Summary

Gets temperature, humidity and pressure from RaspberryPI SenseHat every 1 second. Pulls the same data from openweathermap.org every 5 minutes. Time it gets readings from the SenseHat the script uploads all the information into your MongoDB cluster. The time can be adjusted using the SenseHat joystik. One click up adds one second to the sleep interval. One click down makes one second shorter sleep. Minimum sleep interval is 1 second.

How to use

1. Paste your MongoDB connectio string instead of 'Your connection string' for connection_string constant.
2. Paste your API open weather API key instead of 'Your openweathermap.org API key' for owm_api_key constant.
3. Run "src/service.py". It will start uploading data to your cluster.
4. To cancel press CTRL+C

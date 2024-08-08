import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Get the current timestamp, date, and time
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

# Auto-refresh the page every 2000 milliseconds (2 seconds)
count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

# Implement FizzBuzz logic
if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")

# Construct the file path for the attendance CSV
file_path = "Attendance/Attendance_{date}.csv"

# Read and display the attendance CSV if it exists
try:
    df = pd.read_csv(file_path)
    st.dataframe(df.style.highlight_max(axis=0))
except FileNotFoundError:
    st.write(f"No attendance file found for {date}")

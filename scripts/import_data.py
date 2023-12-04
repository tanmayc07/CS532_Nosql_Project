import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv()

# Set up connection to your MongoDB Atlas cluster
# Replace the placeholders below with your actual connection string
uri = "mongodb+srv://tanmayc:" + os.getenv('CONNECTION_PASS') + "@cluster0.ls88hji.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client[os.getenv('DB_NAME')]
collection = db["stats"]

csv_pref = Path('../data')
# List of your CSV filenames
csv_files = [
    csv_pref / "2012.csv",
    csv_pref / "2013.csv",
    csv_pref / "2014.csv",
    csv_pref / "2015.csv",
    csv_pref / "2016.csv",
    csv_pref / "2017.csv",
    csv_pref / "2018.csv",
    csv_pref / "2019.csv",
    csv_pref / "2020.csv",
    csv_pref / "2021.csv",
    # Add other filenames here
]

# Loop through each CSV file
for file_name in csv_files:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_name)
    
    # Convert DataFrame to a list of dictionaries (one for each row)
    data = df.to_dict(orient='records')
    
    # Insert the data into MongoDB
    collection.insert_many(data)
    
print("Data imported to MongoDB Atlas successfully.")

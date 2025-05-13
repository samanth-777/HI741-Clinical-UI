# stats.py - Generates statistical reports for management users
import pandas as pd

def generate_statistics(patient_data):
    try:
        print("\n=== Management Statistics Report ===")

        patient_data['Visit_time'] = pd.to_datetime(patient_data['Visit_time'], errors='coerce')
        patient_data['Month'] = patient_data['Visit_time'].dt.to_period('M')

        print("\n--- Monthly Visit Trends ---")
        print(patient_data.groupby('Month').size())

        print("\n--- Insurance Distribution ---")
        print(patient_data['Insurance'].value_counts())

        print("\n--- Race Distribution ---")
        print(patient_data['Race'].value_counts())

        print("\n--- Gender Distribution ---")
        print(patient_data['Gender'].value_counts())

        print("\n--- Ethnicity Distribution ---")
        print(patient_data['Ethnicity'].value_counts())

    except Exception as e:
        print(f"Error generating statistics: {e}")

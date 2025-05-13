# patients.py - Manages patient data and operations
import pandas as pd
import random
from datetime import datetime

class PatientManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = pd.read_csv(data_path)
        self._preprocess_dates()

    def _preprocess_dates(self):
        try:
            self.data['Visit_time'] = pd.to_datetime(self.data['Visit_time'], errors='coerce')
        except Exception as e:
            print(f"Date conversion warning: {e}")

    def save(self):
        try:
            self.data.to_csv(self.data_path, index=False)
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_patient(self):
        patient_id = input("Enter Patient_ID: ")
        if patient_id in self.data['Patient_ID'].astype(str).values:
            print("Patient exists. Adding new visit...")
            self._add_visit(patient_id)
        else:
            print("Adding new patient...")
            self._add_new_patient(patient_id)

    def _add_visit(self, patient_id):
        visit = self._collect_visit_info(patient_id)
        self.data = pd.concat([self.data, pd.DataFrame([visit])], ignore_index=True)
        self.save()

    def _add_new_patient(self, patient_id):
        visit = self._collect_visit_info(patient_id)
        self.data = pd.concat([self.data, pd.DataFrame([visit])], ignore_index=True)
        self.save()

    def _collect_visit_info(self, patient_id):
        visit_id = str(random.randint(100000, 999999))
        note_id = str(random.randint(100000, 999999))
        visit_time = input("Enter Visit_time (YYYY-MM-DD): ")
        department = input("Enter department: ")
        race = input("Enter race: ")
        gender = input("Enter gender: ")
        ethnicity = input("Enter ethnicity: ")
        age = input("Enter age: ")
        zip_code = input("Enter zip code: ")
        insurance = input("Enter insurance: ")
        complaint = input("Enter chief complaint: ")
        note_type = input("Enter note type: ")

        return {
            'Patient_ID': patient_id,
            'Visit_ID': visit_id,
            'Visit_time': visit_time,
            'Visit_department': department,
            'Race': race,
            'Gender': gender,
            'Ethnicity': ethnicity,
            'Age': age,
            'Zip_code': zip_code,
            'Insurance': insurance,
            'Chief_complaint': complaint,
            'Note_ID': note_id,
            'Note_type': note_type
        }

    def remove_patient(self):
        patient_id = input("Enter Patient_ID to remove: ")
        if patient_id in self.data['Patient_ID'].astype(str).values:
            self.data = self.data[self.data['Patient_ID'].astype(str) != patient_id]
            self.save()
            print("Patient removed.")
        else:
            print("Patient_ID not found.")

    def retrieve_patient(self):
        patient_id = input("Enter Patient_ID to retrieve: ")
        records = self.data[self.data['Patient_ID'].astype(str) == patient_id]
        if records.empty:
            print("Patient not found.")
        else:
            print(records)

    def count_visits(self, date_str):
        try:
            target_date = pd.to_datetime(date_str)
            return len(self.data[self.data['Visit_time'].dt.date == target_date.date()])
        except Exception as e:
            print(f"Invalid date format: {e}")
            return 0

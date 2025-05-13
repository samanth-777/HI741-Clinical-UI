import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import datetime
import random
import matplotlib.pyplot as plt

class UIApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Clinical Data Warehouse Login")

        self.credentials_df = pd.read_csv("./Credentials.csv", index_col=False)
        self.credentials_df['username'] = self.credentials_df['username'].astype(str).str.strip()
        self.credentials_df['password'] = self.credentials_df['password'].astype(str).str.strip()

        self.patient_data = pd.read_csv("./Patient_data.csv")
        self.patient_data['Visit_time'] = pd.to_datetime(self.patient_data['Visit_time'], errors='coerce')

        try:
            self.notes_data = pd.read_csv("./Notes.csv")
            self.notes_data['Visit_time'] = pd.to_datetime(self.notes_data['Visit_time'], errors='coerce')
        except:
            self.notes_data = pd.DataFrame()

        self.login_frame = tk.Frame(master)
        self.login_frame.pack(padx=10, pady=10)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="e")
        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky="e")

        self.username_entry = tk.Entry(self.login_frame)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.validate_login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=5)

    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        match = self.credentials_df[
            (self.credentials_df["username"] == username) &
            (self.credentials_df["password"] == password)
        ]

        login_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not match.empty:
            role = match.iloc[0]["role"]
            self.log_usage(username, role, login_time, "SUCCESS")
            self.show_role_menu(username, role)
        else:
            self.log_usage(username, "N/A", login_time, "FAILED")
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def log_usage(self, username, role, login_time, status):
        with open("usage_log.csv", "a") as file:
            file.write(f"{username},{role},{login_time},{status}\n")

    def show_role_menu(self, username, role):
        self.login_frame.destroy()
        menu_frame = tk.Frame(self.master)
        menu_frame.pack(padx=10, pady=10)

        tk.Label(menu_frame, text=f"Welcome {username} ({role})").pack()

        actions = []
        if role in ["nurse", "clinician"]:
            actions = ["Retrieve_patient", "Add_patient", "Remove_patient", "Count_visits", "View_Note"]
        elif role == "admin":
            actions = ["Count_visits"]
        elif role == "management":
            actions = ["Generate_key_statistics"]

        for action in actions:
            tk.Button(menu_frame, text=action, command=getattr(self, action.lower())).pack(fill="x", pady=2)

        tk.Button(menu_frame, text="Exit", command=self.master.quit).pack(fill="x", pady=2)

    def count_visits(self):
        date_str = simpledialog.askstring("Count Visits", "Enter date (YYYY-MM-DD):")
        try:
            date_obj = pd.to_datetime(date_str).date()
            count = len(self.patient_data[self.patient_data['Visit_time'].dt.date == date_obj])
            messagebox.showinfo("Visit Count", f"Total visits on {date_str}: {count}")
        except Exception as e:
            messagebox.showerror("Invalid Date", f"Please enter a valid date. Error: {e}")

    def retrieve_patient(self):
        patient_id = simpledialog.askstring("Retrieve Patient", "Enter Patient ID:")
        try:
            records = self.patient_data[self.patient_data['Patient_ID'].astype(str) == patient_id]
            if records.empty:
                messagebox.showinfo("No Record", "No patient found with that ID.")
            else:
                recent = records.sort_values(by='Visit_time', ascending=False).iloc[0]
                info = "\n".join([f"{col}: {recent[col]}" for col in records.columns])
                messagebox.showinfo("Patient Information", info)
        except Exception as e:
            messagebox.showerror("Error", f"Could not retrieve patient. Error: {e}")

    def add_patient(self):
        fields = [
            "Patient_ID", "Visit_time (YYYY-MM-DD)", "Visit_department", "Race",
            "Gender", "Ethnicity", "Age", "Zip_code", "Insurance",
            "Chief_complaint", "Note_type"
        ]
        responses = {}
        for field in fields:
            value = simpledialog.askstring("Add Patient", f"Enter {field}:")
            if value is None:
                return
            responses[field] = value

        visit_id = str(random.randint(100000, 999999))
        note_id = str(random.randint(100000, 999999))

        new_entry = {
            "Patient_ID": responses["Patient_ID"],
            "Visit_ID": visit_id,
            "Visit_time": responses["Visit_time (YYYY-MM-DD)"],
            "Visit_department": responses["Visit_department"],
            "Race": responses["Race"],
            "Gender": responses["Gender"],
            "Ethnicity": responses["Ethnicity"],
            "Age": responses["Age"],
            "Zip_code": responses["Zip_code"],
            "Insurance": responses["Insurance"],
            "Chief_complaint": responses["Chief_complaint"],
            "Note_ID": note_id,
            "Note_type": responses["Note_type"]
        }

        self.patient_data = pd.concat([self.patient_data, pd.DataFrame([new_entry])], ignore_index=True)
        self.patient_data.to_csv("Patient_data.csv", index=False)
        messagebox.showinfo("Success", f"Patient data added successfully with Visit ID {visit_id}.")

    def remove_patient(self):
        patient_id = simpledialog.askstring("Remove Patient", "Enter Patient ID to remove:")
        if not patient_id:
            return
        matches = self.patient_data[self.patient_data['Patient_ID'].astype(str) == patient_id]
        if matches.empty:
            messagebox.showinfo("Not Found", "No patient found with that ID.")
        else:
            self.patient_data = self.patient_data[self.patient_data['Patient_ID'].astype(str) != patient_id]
            self.patient_data.to_csv("Patient_data.csv", index=False)
            messagebox.showinfo("Removed", f"All records for Patient ID {patient_id} removed.")

    def view_note(self):
        if self.notes_data.empty:
            messagebox.showinfo("No Notes", "No clinical notes available.")
            return

        patient_id = simpledialog.askstring("View Note", "Enter Patient ID:")
        date_str = simpledialog.askstring("View Note", "Enter Date (YYYY-MM-DD):")
        try:
            date = pd.to_datetime(date_str).date()
            filtered = self.notes_data[
                (self.notes_data['Patient_ID'].astype(str) == patient_id) &
                (self.notes_data['Visit_time'].dt.date == date)
            ]
            if filtered.empty:
                messagebox.showinfo("No Note", f"No notes found for Patient ID {patient_id} on {date_str}.")
            else:
                notes = "\n\n".join(
                    [f"Type: {row['Note_type']}\nText: {row['Note_text']}" for _, row in filtered.iterrows()]
                )
                messagebox.showinfo("Clinical Notes", notes)
        except Exception as e:
            messagebox.showerror("Error", f"Could not retrieve note. Error: {e}")

    def generate_key_statistics(self):
        try:
            stats = self.patient_data.copy()
            stats['Visit_time'] = pd.to_datetime(stats['Visit_time'], errors='coerce')
            stats['Month'] = stats['Visit_time'].dt.to_period('M')

            fig, axs = plt.subplots(2, 2, figsize=(10, 8))
            axs = axs.flatten()

            stats['Insurance'].value_counts().plot(kind='bar', ax=axs[0], title='Insurance Distribution')
            stats['Race'].value_counts().plot(kind='bar', ax=axs[1], title='Race Distribution')
            stats['Gender'].value_counts().plot(kind='bar', ax=axs[2], title='Gender Distribution')
            stats['Ethnicity'].value_counts().plot(kind='bar', ax=axs[3], title='Ethnicity Distribution')

            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate statistics. Error: {e}")


if __name__ == '__main__':
    root = tk.Tk()
    app = UIApp(root)
    root.mainloop()


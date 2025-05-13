# main.py - Entry point for the program
import argparse
from users import UserManager
from patients import PatientManager
from notes import NoteManager
from stats import generate_statistics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-username", required=True, help="Username")
    parser.add_argument("-password", required=True, help="Password")
    args = parser.parse_args()

    user_manager = UserManager("./PA3_credentials.csv")
    patient_manager = PatientManager("./PA3_data.csv")
    note_manager = NoteManager("./PA3_Notes.csv")

    user = user_manager.authenticate(args.username, args.password)
    if not user:
        print("Invalid credentials. Access denied.")
        return

    print(f"\nWelcome {user.username}! Role: {user.role}")
    if user.role.strip().lower() == "management":
        generate_statistics(patient_manager.data)

    elif user.role == "admin":
        date_str = input("Enter date (YYYY-MM-DD): ")
        count = patient_manager.count_visits(date_str)
        print(f"Total visits on {date_str}: {count}")

    elif user.role in ["nurse", "clinician"]:
        while True:
            action = input("\nChoose action: add, remove, retrieve, count, view, stop: ").lower()
            if action == "add":
                patient_manager.add_patient()
            elif action == "remove":
                patient_manager.remove_patient()
            elif action == "retrieve":
                patient_manager.retrieve_patient()
            elif action == "count":
                date_str = input("Enter date (YYYY-MM-DD): ")
                print(f"Visits: {patient_manager.count_visits(date_str)}")
            elif action == "view":
                date_str = input("Enter date (YYYY-MM-DD): ")
                note_manager.get_notes_by_date(date_str)
            elif action == "stop":
                print("Session ended.")
                break
            else:
                print("Invalid action.")

if __name__ == "__main__":
    main()

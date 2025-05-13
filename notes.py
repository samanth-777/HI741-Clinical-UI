# notes.py - Handles clinical note operations
import pandas as pd

class NoteManager:
    def __init__(self, notes_path):
        try:
            self.notes = pd.read_csv(notes_path)
            if 'Visit_time' in self.notes.columns:
                self.notes['Visit_time'] = pd.to_datetime(self.notes['Visit_time'], errors='coerce')
        except FileNotFoundError:
            print(f"Error: Notes file not found at {notes_path}")
            self.notes = pd.DataFrame()

    def get_notes_by_date(self, date_str):
        try:
            target_date = pd.to_datetime(date_str)
            if 'Visit_time' not in self.notes.columns:
                print("Visit_time column missing in notes.")
                return

            filtered = self.notes[self.notes['Visit_time'].dt.date == target_date.date()]
            if filtered.empty:
                print(f"No notes found for {date_str}.")
            else:
                print(f"\n--- Notes for {date_str} ---")
                for _, note in filtered.iterrows():
                    print(f"Patient ID: {note['Patient_ID']} | Visit ID: {note['Visit_ID']} | Note ID: {note['Note_ID']}")
                    print(f"Type: {note['Note_type']}")
                    note_text = note['Note_text']
                    if len(note_text) > 200:
                        print(f"Text (truncated): {note_text[:200]}...\n")
                    else:
                        print(f"Text: {note_text}\n")
        except Exception as e:
            print(f"Error viewing notes: {e}")

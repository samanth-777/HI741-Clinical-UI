Clinical Data Warehouse UI

This is a Python-based GUI application. It simulates a Clinical Data Warehouse system with **role-based access**, **patient record management**, **notes viewing**, and **key visit statistics** – all through a user-friendly Tkinter GUI.


## 🚀 Features

### 🔐 Role-Based Access Control
- `admin`, `nurse`, `clinician`, and `management` users authenticate via GUI.
- Credentials are stored in `Credentials.csv`.

### 🩺 Patient Interaction Tools (Nurse/Clinician)
- **Add Patient**: Add new patient visit records
- **Retrieve Patient**: View most recent visit data by Patient ID
- **Remove Patient**: Delete all records for a Patient ID
- **View Note**: View visit notes based on Patient ID and date

### 📊 Operational Tools
- **Count Visits**: See visit count for a specific date (accessible by all roles)
- **Generate Key Statistics** *(Management Only)*:
  - Visualizes data distributions: Race, Gender, Insurance, Ethnicity

### 📝 Logging
- All login attempts (successful or failed) are logged in `usage_log.csv`
- Updated patient data is written to `Patient_data.csv` after modifications

---

## ▶️ How to Run

1. Clone the repo:
```bash
git clone https://github.com/your-username/HI741-Clinical-UI.git
cd HI741-Clinical-UI

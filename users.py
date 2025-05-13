# users.py - Handles user authentication and access control
import pandas as pd

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class UserManager:
    def __init__(self, credentials_path):
        self.users = self._load_users(credentials_path)

    def _load_users(self, path):
        users = {}
        try:
            df = pd.read_csv(path)
            for _, row in df.iterrows():
                username = row['username']
                users[username] = {
                    'password': row['password'],
                    'role': row['role']
                }
        except FileNotFoundError:
            print(f"Credential file not found at: {path}")
        return users

    def authenticate(self, username, password):
        user_record = self.users.get(username)
        if user_record and user_record['password'] == password:
            return User(username, user_record['role'])
        return None

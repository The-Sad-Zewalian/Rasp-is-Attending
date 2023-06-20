import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

class DatabaseManager:
    persons = {}
    def __init__(self):
        cred = credentials.Certificate("")
        firebase_admin.initialize_app(cred ,{'databaseURL': ''})
        self.ref = db.reference('Attendance')

    def add_attendance_now(self, name ,ignore_day_duplicate = False ):
        today = datetime.date.today()
        if self.persons.get(name) and self.persons[name] == today and ignore_day_duplicate:
            print("Already registered today")
            return
        timestamp =  datetime.datetime.now().strftime('%m-%d %H:%M:%S')

        self.persons[name] = today
        # Push the attendance data with the timestamp as the child name
        attendance_ref = self.ref.child(timestamp)
        attendance_ref.set({
            "name": name
        })
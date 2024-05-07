import datetime
import psycopg2
from public_page import *
from profile_page import *

def validate_date_of_birth(dob_str):
    try:
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
        if dob > datetime.date.today():
            raise ValueError("Date of birth cannot be in the future.")
        return dob
    except ValueError as e:
        print(f"Invalid date of birth: {str(e)}")
        return None
    
def validate_int(user_id):
    try:
        user_id = int(user_id)
        return True
    except ValueError:
        return False


def login(cursor,conn,user_data):
    user_id, F_name, l_name, password, email, DOB, phone = user_data
    print(f"Your ID: {user_id} , Name: {F_name} {l_name}")
    print(f"Email: {email} , Date of Birth: {DOB} , Phone: {phone} \n")
    command = "1"
    while command == "1" or command == "2":
        print("\nEnter 1 to see friends post")
        print("Enter 2 to see your activity")
        print("Enter anything to logout")
        command = input("Enter command ").strip()
        if command == "1":
            home(cursor,conn,user_id)
        if command == "2":
            profile_info(cursor,conn,user_id)

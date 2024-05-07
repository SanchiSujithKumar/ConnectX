import datetime
import psycopg2
from signUp import *
from signIn import *

conn = psycopg2.connect(database='facebookdb',
						host="localhost",
						user="postgres",
						password="123456",
						port=5432) 
cursor = conn.cursor()

def validate_int(user_id):
    try:
        user_id = int(user_id)
        return True
    except ValueError:
        return False

command = "1"
while command == "1" or command == "2" :
    print("\nEnter 1 to signin")
    print("Enter 2 to signup")
    print("Enter anything to exit")
    command = input("Enter command ").strip()

    if command == "1":

        logged_in=False
        while not logged_in:
            user_id = input("Enter your user ID: ")
            if validate_int(user_id):
                password = input("Enter your password: ")
                cursor.execute("SELECT passwd FROM user_tb WHERE user_id = %s", (user_id,))
                stored_password = cursor.fetchone()
                if stored_password:
                    stored_password = stored_password[0]
                    if (password == stored_password):
                        cursor.execute("SELECT * FROM user_tb WHERE user_id = %s", (user_id,))
                        user_data = cursor.fetchone()
                        logged_in=True
                        login(cursor,conn,user_data)
                    else:
                        print("Incorrect password. Please try again.\n")
                else:
                    print("User not found with the provided user ID. Please try again.")
            else:
                print("Enter an integer")
    
    if command == "2":
        create_account(cursor,conn)
        
conn.close()


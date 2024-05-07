import datetime
import psycopg2

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

def create_account(cursor,conn):
        new_user_data = {
            'user_ID': None,
            'first_name': None,
            'last_name': None,
            'password': None,
            'email': None,
            'DOB': None,
            'phone': None,
        }
        while new_user_data['user_ID'] is None:
            user_id_input = input("Enter your id: ")
            if validate_int(user_id_input):
                cursor.execute("SELECT COUNT(*) FROM user_tb WHERE user_id = %s", (user_id_input,))
                user_id_count = cursor.fetchone()[0]
                if user_id_count == 0:
                    new_user_data['user_ID'] = int(user_id_input)
                else:
                    print("User ID already exists. Please enter a different ID.")
            else:
                print("Enter an integer")

        while new_user_data['first_name'] is None:
            first_name_input = input("Enter your first name: ").strip()
            if first_name_input.strip():
                new_user_data['first_name'] = first_name_input
            else:
                print("Invalid first name. Please enter a valid name.")

        while new_user_data['last_name'] is None:
            last_name_input = input("Enter your last name: ").strip()
            if last_name_input.strip():
                new_user_data['last_name'] = last_name_input
            else:
                print("Invalid last name. Please enter a valid name.")

        while new_user_data['password'] is None:
            password_input = input("Enter your password: ")
            if len(password_input) < 8:
                print("Password must be at least 8 characters long.")
            elif not any(c.isupper() for c in password_input):
                print("Password must contain at least one uppercase letter.")
            elif not any(c.islower() for c in password_input):
                print("Password must contain at least one lowercase letter.")
            elif not any(c.isdigit() for c in password_input):
                print("Password must contain at least one digit.")
            elif not any(c in "!@#$%^&*()_+[]{}|;:,.<>?-=" for c in password_input):
                print("Password must contain at least one special character (!@#$%^&*()_+[]{}|;:,.<>?-=).")
            else:
                new_user_data['password'] = password_input

        while new_user_data['email'] is None:
            email_input = input("Enter your email: ").strip()
            if "@" in email_input and "." in email_input:
                new_user_data['email'] = email_input
            else:
                print("Invalid email. Please enter a valid email address.")


        while new_user_data['DOB'] is None:
            dob_input = input("Enter your date of birth (YYYY-MM-DD): ").strip()
            if(validate_date_of_birth(dob_input)):
                new_user_data['DOB'] = dob_input


        while new_user_data['phone'] is None:
            phone_input = input("Enter your phone number: ").strip()
            if phone_input.isdigit() and len(phone_input) >= 10:
                new_user_data['phone'] = phone_input
            else:
                print("Invalid phone number. Please enter a valid numeric value with at least 10 digits.")

        sql = "INSERT INTO user_tb (user_id,F_name, l_name, passwd, email, DOB, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (new_user_data['user_ID'],new_user_data['first_name'], new_user_data['last_name'],new_user_data['password'], new_user_data['email'], new_user_data['DOB'], new_user_data['phone'])
        cursor.execute(sql, val)
        conn.commit()
        print("your has been created now can sign in")


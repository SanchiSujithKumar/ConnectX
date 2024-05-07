import datetime
import psycopg2
from post_page import *

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

def profile_info(cursor,conn,user_id):
    command="2"
    while command=="1" or command=="2" or command=="3":
        print("\nEnter 1 to see post")
        print("Enter 2 to see friends")
        print("Enter 3 to see pages")
        print("Enter anything to go back")
        command = input("Enter command ").strip()

        if command == "1":
            posts(cursor,conn,user_id)
        if command == "2":

            cursor.execute("SELECT u.user_id FROM user_tb u INNER JOIN Friend f ON u.user_id = f.Friend_id WHERE f.user_id = %s", (user_id,))
            user_friends1 = cursor.fetchall()
            cursor.execute("SELECT u.user_id FROM user_tb u INNER JOIN Friend f ON u.user_id = f.user_id WHERE f.Friend_id = %s", (user_id,))
            user_friends2 = cursor.fetchall()
            user_friends11=[]
            for friend_id in user_friends1:
                user_friends11.append(friend_id[0])
            user_friends22=[]
            for friend_id in user_friends2:
                user_friends22.append(friend_id[0])
            user_friends=[]
            for friend_id in user_friends11:
                if friend_id in user_friends22:
                    user_friends.append(friend_id)

            
            if user_friends:
                print("\nFriends:\n")
                for friend in user_friends:
                    cursor.execute("SELECT u.user_id, u.F_name, u.l_name FROM user_tb u WHERE u.user_id = %s", (friend,))
                    user_friend = cursor.fetchone()
                    friend_id, friend_F_name, friend_l_name = user_friend
                    print(f"Friend ID: {friend_id} ,  Friend Name:  {friend_F_name} {friend_l_name} ")

            user_friends111=[]
            for friend in user_friends11:
                if friend not in user_friends:
                    user_friends111.append(friend)
            if user_friends111:
                print("\nFriends request sent :\n")
                for friend in user_friends111 :
                    cursor.execute("SELECT u.user_id, u.F_name, u.l_name FROM user_tb u WHERE u.user_id = %s", (friend,))
                    user_friend = cursor.fetchone()
                    friend_id, friend_F_name, friend_l_name = user_friend
                    print(f"Friend ID: {friend_id} ,  Friend Name:  {friend_F_name} {friend_l_name} ")
            
            user_friends111=[]
            for friend in user_friends22:
                if friend not in user_friends:
                    user_friends111.append(friend)
            if user_friends111:
                print("\nFriends request recieved :\n")
                for friend in user_friends111 :
                    cursor.execute("SELECT u.user_id, u.F_name, u.l_name FROM user_tb u WHERE u.user_id = %s", (friend,))
                    user_friend = cursor.fetchone()
                    friend_id, friend_F_name, friend_l_name = user_friend
                    print(f"Friend ID: {friend_id} ,  Friend Name:  {friend_F_name} {friend_l_name} ")
            
            another_action = input("\nDo you want to unfriend (yes/no)? ").strip().lower()
            while another_action == 'yes':
                friend_id=input("Enter friend_id ").strip()
                if friend_id :
                    cursor.execute("SELECT u.user_id FROM user_tb u INNER JOIN Friend f ON u.user_id = f.Friend_id WHERE f.user_id = %s and f.Friend_id=%s", (user_id,friend_id,))
                    post_likes = cursor.fetchall()
                    if post_likes:
                        print("\n this friend is removed from friends list")
                        cursor.execute("DELETE FROM Friend WHERE friend_id =%s and user_id=%s", (friend_id,user_id,))
                        cursor.execute("DELETE FROM Friend WHERE friend_id =%s and user_id=%s", (user_id,friend_id,))
                        conn.commit()
                    else:
                        print("incorrect an friend_id ")
                another_action = input("\nDo you want to unfriend (yes/no)? ").strip().lower()
            
            another_action = input("\nDo you want to add a friend (yes/no)? ").strip().lower()
            while another_action == 'yes':
                friend_id=input("Enter friend_id ").strip()
                if friend_id :
                    cursor.execute("SELECT u.user_id FROM user_tb u INNER JOIN Friend f ON u.user_id = f.Friend_id WHERE f.user_id = %s and f.Friend_id=%s", (user_id,friend_id,))
                    post_likes = cursor.fetchall()
                    if not post_likes:
                        try:
                            print("\n this friend is added to friends list")
                            cursor.execute("INSERT INTO Friend (Friend_id, user_id) VALUES (%s, %s)", (friend_id,user_id,))
                            conn.commit()
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print("Failed to insert the image. An integrity constraint violation occurred.")
                        except psycopg2.Error as e:
                            conn.rollback()
                            print(f"Error: {e}")
                    else:
                        print("incorrect an friend_id ")
                another_action = input("\nDo you want to add another friend (yes/no)? ").strip().lower()

        if command == "3":
            cursor.execute("SELECT p.page_id, p.page_name, p.DOC, p.createdBy, p.email, p.page_content,p.totalLikes FROM user_tb,Pages p WHERE p.createdBy = user_tb.user_id and p.createdBy = %s", (user_id,))
            user_pages = cursor.fetchall()
            if user_pages:
                print("\nYour pages:")
                for page in user_pages:
                    page_id, page_name, DOC, createdBy, email, page_content,totalLikes = page
                    print(f"Page id: {page_id} Page name: {page_name} Created on:{DOC} Created by: {createdBy} Email id of page: {email} About: {page_content} Likes: {totalLikes} ")

            cursor.execute("SELECT p.page_id, p.page_name, p.DOC, p.createdBy, p.email, p.page_content,p.totalLikes FROM Pages p ")
            user_pages = cursor.fetchall()
            if user_pages:
                print("All pages:")
                for page in user_pages:
                    page_id, page_name, DOC, createdBy, email, page_content,totalLikes = page
                    print(f"Page id: {page_id} Page name: {page_name} Created on:{DOC} Created by: {createdBy} Email id of page: {email} About: {page_content} Likes: {totalLikes} ")

            cursor.execute("SELECT p.page_id, p.page_name, p.page_content FROM Pages p INNER JOIN Page_likes pl ON p.page_id = pl.page_id WHERE pl.user_id = %s", (user_id,))
            user_liked_pages = cursor.fetchall()
            if user_liked_pages:
                print("\nPages liked by you:")
                for liked_page in user_liked_pages:
                    page_id, page_name, page_content = liked_page
                    print(f"Page ID: {page_id} , Page Name: {page_name} , Content: {page_content}")
            
            another_action = input("\nDo you want to unlike pages (yes/no)? ").strip().lower()
            while another_action == 'yes':
                page_id=input("Enter page_id ").strip()
                if page_id :
                    cursor.execute("SELECT p.page_id FROM Pages p INNER JOIN Page_likes pl ON p.page_id = pl.page_id WHERE pl.user_id = %s and p.page_id=%s", (user_id,page_id,))
                    post_likes = cursor.fetchall()
                    if post_likes:
                        print("\n this Page like is removed ")
                        cursor.execute("DELETE FROM Page_likes WHERE user_id =%s and page_id=%s", (user_id,page_id,))
                        conn.commit()
                    else:
                        print("incorrect an page_id ")
                another_action = input("\nDo you want to unlike pages (yes/no)? ").strip().lower()
            
            another_action = input("\nDo you want to like some pages (yes/no)? ").strip().lower()
            while another_action == 'yes':
                page_id=input("Enter page_id ").strip()
                if page_id :
                    cursor.execute("SELECT p.page_id FROM Pages p INNER JOIN Page_likes pl ON p.page_id = pl.page_id WHERE pl.user_id = %s and pl.page_id=%s", (user_id,page_id,))
                    post_likes = cursor.fetchall()
                    if not post_likes:
                        try:
                            print("\n this Page liked")
                            cursor.execute("INSERT INTO Page_likes (user_id, page_id) VALUES (%s, %s)", (user_id,page_id,))
                            conn.commit()
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print("Failed to insert the image. An integrity constraint violation occurred.")
                        except psycopg2.Error as e:
                            conn.rollback()
                            print(f"Error: {e}")
                    else:
                        print("incorrect an page_id ")
                another_action = input("\nDo you want to like some pages (yes/no)? ").strip().lower()
            
            another_action = input("\nDo you want to create page (yes/no)? ").strip().lower()
            if another_action == 'yes':
                page_name = input("Enter the name of the new page: ")
                while not page_name:
                    print("Page name is a required field. Please enter a valid page name.")
                    page_name = input("Enter the name of the new page: ")
                doc = datetime.date.today()
                created_by = user_id  
                email = None
                while email is None:
                    email_input = input("Enter the email address: ")
                    if "@" in email_input and "." in email_input:
                        email = email_input
                    else:
                        print("Invalid email. Please enter a valid email address.")
                        continue
                page_content = input("Enter the page content: ")
                try:
                    cursor.execute("SELECT max(page_id) FROM Pages")
                    current = cursor.fetchone()
                    page_id = current[0] + 1 if current[0] is not None else 1

                    sql = "INSERT INTO Pages (page_id, page_name, DOC, createdBy, email, page_content, totalLikes) VALUES (%s, %s, %s, %s, %s, %s, 0)"
                    val = (page_id, page_name, doc, created_by, email, page_content)
                    cursor.execute(sql, val)
                    conn.commit()
                    print("Page inserted successfully.")
                except psycopg2.IntegrityError as e:
                    conn.rollback()
                    print("Failed to insert the page. An integrity constraint violation occurred.")
                except psycopg2.Error as e:
                    conn.rollback()
                    print(f"Error: {e}")
                
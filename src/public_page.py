import datetime
import psycopg2

def home(cursor,conn,user_id):
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
            print("posts posted by your friends: ")
            for friend_id in user_friends:
                cursor.execute("SELECT p.post_id, p.post_content, p.post_date, p.post_likes, count(c.post_id), count(s.post_id)  FROM Posts p LEFT JOIN Comments c ON p.post_id = c.post_id LEFT JOIN Shares s ON p.post_id = s.post_id WHERE p.user_id = %s GROUP BY p.post_id, p.post_content, p.post_date, p.post_likes", (friend_id,))
                user_posts_details = cursor.fetchall()
                if user_posts_details:
                    for post in user_posts_details:
                        print(f"friend_id:{friend_id} post_id: {post[0]} , post_content: {post[1]} , post_Date: {post[2]} , num of likes: {post[3]}, num of comments: {post[4]} , num of shares: {post[5]}")

            print("posts shared by your friends: ")
            for friend_id in user_friends:
                cursor.execute("SELECT p.post_id, p.post_content, p.post_date, p.post_likes, count(c.post_id), count(s.post_id)  FROM Posts p LEFT JOIN Comments c ON p.post_id = c.post_id LEFT JOIN Shares s ON p.post_id = s.post_id WHERE s.user_id = %s GROUP BY p.post_id, p.post_content, p.post_date, p.post_likes", (friend_id,))
                user_posts_details = cursor.fetchall()
                if user_posts_details:
                    for post in user_posts_details:
                        print(f"friend_id:{friend_id} post_id: {post[0]} , post_content: {post[1]} , post_Date: {post[2]} , num of likes: {post[3]}, num of comments: {post[4]} , num of shares: {post[5]}")

            another_action = input("\nDo you want to like post (yes/no)? ").strip().lower()
            while another_action == 'yes':
                post_id_like=input("Enter post_id ").strip()
                if post_id_like :
                    cursor.execute("SELECT pl.user_id FROM Posts p INNER JOIN Posts_likes pl ON p.post_id = pl.post_id WHERE p.post_id = %s and pl.user_id=%s", (post_id_like,user_id,))
                    post_likes = cursor.fetchall()
                    if not post_likes:
                        try:
                            cursor.execute("INSERT INTO Posts_likes (post_id, user_id) VALUES (%s, %s)", (post_id_like, user_id,))
                            print("You liked a post")
                            cursor.execute("UPDATE Posts SET post_likes = post_likes + 1 WHERE post_id = %s", (post_id_like,))
                            conn.commit()
                        except psycopg2.IntegrityError as e:
                            conn.rollback()  
                            print("Failed to like this post. An integrity constraint violation occurred.")
                        except psycopg2.Error as e:
                            conn.rollback()
                            print(f"Error: {e}")
                    else:
                        print("incorrect an post_id or already liked")
                another_action = input("\nDo you want to like another post (yes/no)? ").strip().lower()

            another_action = input("\nDo you want to add a comment (yes/no)? ").strip().lower()
            while another_action == 'yes':
                post_id_like=input("Enter post_id ").strip()
                if post_id_like :
                    cursor.execute("SELECT p.post_id FROM Posts p WHERE p.post_id = %s", (post_id_like,))
                    post_likes = cursor.fetchall()
                     
                    if post_likes:
                        comment_text = input("Enter your comment: ")
                        cursor.execute("SELECT max(comment_id) FROM Comments")
                        current = cursor.fetchone()
                        comment_id = current[0] + 1 if current[0] is not None else 1
                        commentdate = datetime.date.today() 
                        try:
                            cursor.execute("INSERT INTO Comments (comment_id, commentdate, post_id, user_id, comment_text) VALUES (%s, %s, %s, %s, %s)", (comment_id, commentdate, post_id_like, user_id, comment_text,))
                            conn.commit()
                            print("Comment inserted successfully.")
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print("Failed to insert the comment. An integrity constraint violation occurred.")
                        except psycopg2.Error as e:
                            conn.rollback()
                            print(f"Error: {e}")
                    else:
                        print("incorrect an post_id ")
                another_action = input("\nDo you want to add another comment (yes/no)? ").strip().lower()

            another_action = input("\nDo you want to see comments of a post (yes/no)? ").strip().lower()
            while another_action == 'yes':
                post_id_like=input("Enter post_id ").strip()
                if post_id_like :
                    cursor.execute("SELECT p.post_id FROM Posts p WHERE p.post_id=%s", (post_id_like,))
                    post_likes = cursor.fetchall()
                    if post_likes:
                        cursor.execute("SELECT c.comment_id, c.commentdate, c.post_id, c.user_id, c.comment_text FROM Comments c WHERE c.post_id = %s", (post_id_like,))
                        user_comments = cursor.fetchall()
                        if user_comments:
                            print("\n Comments:")
                            for comment in user_comments:
                                comment_id, commentdate, post_id, user_id, comment_text = comment
                                print(f"Comment ID: {comment_id} , Comment Date: {commentdate} , Post ID: {post_id} ,user  ID: {user_id} , Comment text: {comment_text}")
                            another_action = input("\nDo you want to like a comments (yes/no)? ").strip().lower()
                            while another_action == 'yes':
                                comment_id=input("Enter comment_id ").strip()
                                if comment_id:
                                    cursor.execute("SELECT cl.comment_id FROM Commentlikes cl  WHERE cl.user_id = %s and cl.comment_id=%s", (user_id,comment_id,))
                                    comment_likes = cursor.fetchall()
                                    if not comment_likes:
                                        try:
                                            cursor.execute("INSERT INTO Commentlikes (comment_id, user_id) VALUES (%s, %s)", (comment_id, user_id))
                                            conn.commit()
                                            print("Liked the comment successfully.")
                                        except psycopg2.IntegrityError as e:
                                            conn.rollback()
                                            print("Failed to insert the comment. An integrity constraint violation occurred.")
                                        except psycopg2.Error as e:
                                            conn.rollback()
                                            print(f"Error: {e}")
                                    else:
                                        print("incorrect an comment_id or already liked")
                                another_action = input("\nDo you want to like another comment (yes/no)? ").strip().lower()
                    else:
                        print("incorrect an post_id")
                another_action = input("\nDo you want to see comments of another post (yes/no)? ").strip().lower()
            
            another_action = input("\nDo you want to share post (yes/no)? ").strip().lower()
            while another_action == 'yes':
                post_id_like=input("Enter post_id ").strip()
                if post_id_like :
                    cursor.execute("SELECT s.user_id FROM Posts p INNER JOIN shares s ON p.post_id = s.post_id WHERE p.post_id = %s and s.user_id=%s", (post_id_like,user_id,))
                    post_likes = cursor.fetchall()
                    if not post_likes:
                        try:
                            cursor.execute("INSERT INTO shares (post_id, user_id, count) VALUES (%s, %s, 1)", (post_id_like, user_id,))
                            print("You shared a post")
                            cursor.execute("UPDATE Posts SET post_likes = post_likes + 1 WHERE post_id = %s", (post_id_like,))
                            conn.commit()
                        except psycopg2.IntegrityError as e:
                            conn.rollback()  
                            print("Failed to share this post. An integrity constraint violation occurred.")
                        except psycopg2.Error as e:
                            conn.rollback()
                            print(f"Error: {e}")
                    else:
                        print("incorrect an post_id or already shared")
                another_action = input("\nDo you want to share another post (yes/no)? ").strip().lower()
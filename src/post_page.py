import datetime
import psycopg2

def posts(cursor,conn,user_id):
    command="1"
    while command=="1" or command=="2" or command=="3" or command=="4" or command=="5":
        print("\nEnter 1 to see your post")
        print("Enter 2 to see posts liked by you")
        print("Enter 3 to see posts shared by you")
        print("Enter 4 to see your comments")
        print("Enter 5 to see comments liked by you")
        print("Enter anything to go back")
        command = input("Enter command ").strip()

        if command == "1":
            cursor.execute("SELECT p.post_id, p.post_content, p.post_date, p.post_likes, count(c.post_id), count(s.post_id)  FROM Posts p LEFT JOIN Comments c ON p.post_id = c.post_id LEFT JOIN Shares s ON p.post_id = s.post_id WHERE p.user_id = %s GROUP BY p.post_id, p.post_content, p.post_date, p.post_likes", (user_id,))
            user_posts_details = cursor.fetchall()
            user_posts=[]
            if user_posts_details:
                print("\nYour Post details:\n")
                for post in user_posts_details:
                    user_posts.append(post[0])
                    print(f"post_id: {post[0]} , post_content: {post[1]} , post_Date: {post[2]} , num of likes: {post[3]}, num of comments: {post[4]} , num of shares: {post[5]}")

            cursor.execute("SELECT p.photo_id, p.image_content, p.post_id FROM Photos p INNER JOIN Posts ps ON p.post_id = ps.post_id WHERE ps.user_id = %s", (user_id,))
            user_photos = cursor.fetchall()
            if user_photos:
                print("\nYour Photos:")
                for photo in user_photos:
                    photo_id, image_content, post_id = photo
                    print(f"Photo ID: {photo_id} , Image Content: {image_content} , Associated Post ID: {post_id}")
            
            another_action = input("\nDo you want to see who liked your post (yes/no)? ").strip().lower()
            if another_action == 'yes':
                for post in user_posts:
                    cursor.execute("SELECT pl.user_id FROM Posts p INNER JOIN Posts_likes pl ON p.post_id = pl.post_id WHERE p.post_id = %s", (post,))
                    post_likes = cursor.fetchall()
                    if post_likes:
                        print(f"{post} this post is liked by:")
                        for like in post_likes:
                            post_liked = like
                            print(f"Post ID: {post} , post liked by: {post_liked[0]}")
                    

            another_action = input("\nDo you want to see who commented your post (yes/no)? ").strip().lower()
            if another_action == 'yes':
                for post in user_posts:
                    cursor.execute("SELECT c.user_id, c.comment_text FROM Posts p INNER JOIN Comments c ON p.post_id = c.post_id WHERE p.post_id = %s", (post,))
                    post_likes = cursor.fetchall()
                    if post_likes:
                        print(f"{post} this post is commented by:")
                        for like in post_likes:
                            post_liked,comment_text = like
                            print(f"Post ID: {post} , post commented by: {post_liked} , text: {comment_text}")
            
            another_action = input("\nDo you want to see who shared your post (yes/no)? ").strip().lower()
            if another_action == 'yes':
                for post in user_posts:
                    cursor.execute("SELECT s.user_id FROM Posts p INNER JOIN shares s ON p.post_id = s.post_id WHERE p.post_id = %s", (post,))
                    post_likes = cursor.fetchall()
                    if post_likes:
                        print(f"{post} this post is shared by:")
                        for like in post_likes:
                            post_liked = like
                            print(f"Post ID: {post} , post shared by: {post_liked[0]}")
            
            another_action = input("\nDo you want to insert your post (yes/no)? ").strip().lower()
            while another_action == 'yes':
                cursor.execute("SELECT max(post_id) FROM Posts")
                current = cursor.fetchone()
                post_id = current[0] + 1 if current[0] is not None else 1

                post_content = input("\nEnter your post content: ")
                post_date = datetime.date.today()

                try:
                    sql = "INSERT INTO Posts (post_id, post_content, post_Date, user_id, post_likes) VALUES (%s, %s, %s, %s, %s)"
                    val = (post_id, post_content, post_date, user_id, 0)
                    cursor.execute(sql, val)
                    conn.commit()
                    print("Post insertion completed successfully.")
                    another_action = input("\nDo you want to insert photos to this post (yes/no)? ").strip().lower()
                    while another_action == 'yes':
                        cursor.execute("SELECT max(photo_id) FROM Photos")
                        current = cursor.fetchone()
                        photo_id = current[0] + 1 if current[0] is not None else 1

                        image_content = input("Enter the image content: ")
                        try:
                            sql = "INSERT INTO Photos (photo_id, image_content, post_id) VALUES (%s, %s, %s)"
                            val = (photo_id, image_content, post_id)
                            cursor.execute(sql, val)
                            conn.commit()
                            print("Image inserted successfully.")
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print("Failed to insert the image. An integrity constraint violation occurred.")
                        except psycopg2.Error as e:
                            conn.rollback()
                            print(f"Error: {e}")
                        another_action = input("\nDo you want to insert another photo to this post (yes/no)? ").strip().lower()
                except psycopg2.IntegrityError as e:
                    conn.rollback()
                    print("Post insertion failed. An integrity constraint violation occurred.")
                except psycopg2.Error as e:
                    conn.rollback()
                    print(f"Error: {e}")
                another_action = input("\nDo you want to insert your post (yes/no)? ").strip().lower()
            
            another_action = input("\nDo you want to delete your post (yes/no)? ").strip().lower()
            while another_action == 'yes':
                post_id=input("Enter post_id ").strip()
                if post_id :
                    cursor.execute("SELECT p.post_id FROM Posts p WHERE p.post_id = %s and p.user_id =%s", (post_id,user_id,))
                    post_likes = cursor.fetchall()
                    if post_likes:
                        print("\n this post is deleted ")
                        cursor.execute("SELECT cl.comment_id FROM Comments c INNER JOIN Commentlikes cl ON c.comment_id = cl.comment_id WHERE c.post_id = %s ", (post_id,))
                        comment_likes = cursor.fetchall()
                        for like in comment_likes:
                            cursor.execute("DELETE FROM Commentlikes WHERE comment_id =%s", (like,))
                        cursor.execute("DELETE FROM Comments WHERE post_id =%s", (post_id,))
                        cursor.execute("DELETE FROM shares WHERE post_id =%s", (post_id,))
                        cursor.execute("DELETE FROM Photos WHERE post_id =%s", (post_id,))
                        cursor.execute("DELETE FROM Posts_likes WHERE post_id =%s", (post_id,))
                        cursor.execute("DELETE FROM Posts WHERE post_id =%s", (post_id,))
                        conn.commit()
                    else:
                        print("incorrect an post_id ")
                another_action = input("\nDo you want to delete your post (yes/no)? ").strip().lower()
            
        if command == "2":
            cursor.execute("SELECT p.post_id, p.post_content FROM Posts p INNER JOIN Posts_likes pl ON p.post_id = pl.post_id WHERE pl.user_id = %s", (user_id,))
            post_likes = cursor.fetchall()
            if post_likes:
                print("\nPosts liked by you:")
                for like in post_likes:
                    post_id, post_content = like
                    print(f"Post ID: {post_id} , post content: {post_content}")

            another_action = input("\nDo you want to remove your like (yes/no)? ").strip().lower()
            while another_action == 'yes':
                post_id=input("Enter post_id ").strip()
                if post_id :
                    cursor.execute("SELECT p.post_id FROM Posts p INNER JOIN Posts_likes pl ON p.post_id = pl.post_id WHERE pl.user_id = %s and pl.post_id=%s", (user_id,post_id,))
                    post_likes = cursor.fetchall()
                    if post_likes:
                        print("\n this post like is removed ")
                        cursor.execute("UPDATE Posts SET post_likes = post_likes - 1 WHERE post_id = %s ", (post_id,))
                        cursor.execute("DELETE FROM Posts_likes WHERE post_id =%s and user_id=%s", (post_id,user_id))
                        conn.commit()
                    else:
                        print("incorrect an post_id ")
                another_action = input("\nDo you want to remove your like (yes/no)? ").strip().lower()

        if command == "3":
            cursor.execute("select p.post_id, p.post_content, p.post_Date, p.user_id ,s.count from posts p LEFT JOIN shares s ON p.post_id = s.post_id where s.user_id = %s", (user_id,))
            shared_posts = cursor.fetchall()
            if shared_posts:
                    print("\nPosts shared by you:")
                    for shared_post in shared_posts:
                        post_id, post_content, post_Date, posted_by, post_count = shared_post
                        print(f"Post ID: {post_id} , Post Content: {post_content} , Posted on: {post_Date} , Posted by: {posted_by} , num of shares: {post_count}")
            
            another_action = input("\nDo you want to unshare this (yes/no)? ").strip().lower()
            while another_action == 'yes':
                post_id=input("Enter post_id ").strip()
                if post_id :
                    cursor.execute("select p.post_id from posts p LEFT JOIN shares s ON p.post_id = s.post_id where s.user_id = %s and s.post_id=%s", (user_id,post_id,))
                    post_likes = cursor.fetchall()
                    if post_likes:
                        print("\n this post like is unshared ")
                        cursor.execute("DELETE FROM shares WHERE post_id =%s", (post_id,))
                        conn.commit()
                    else:
                        print("incorrect an post_id ")
                another_action = input("\nDo you want to unshare this (yes/no)? ").strip().lower()
            
        if command == "4":
            cursor.execute("SELECT c.comment_id, c.commentdate, c.post_id, c.user_id, c.comment_text FROM Comments c WHERE c.user_id = %s", (user_id,))
            user_comments = cursor.fetchall()
            if user_comments:
                print("\nYour Comments:")
                for comment in user_comments:
                    comment_id, commentdate, post_id, user_id, comment_text = comment
                    print(f"Comment ID: {comment_id} , Comment Date: {commentdate} , Post ID: {post_id} , Comment text: {comment_text}")

            another_action = input("\nDo you want to uncomment this (yes/no)? ").strip().lower()
            while another_action == 'yes':
                comment_id=input("Enter comment_id ").strip()
                if comment_id :
                    cursor.execute("SELECT c.comment_id FROM Comments c WHERE c.user_id = %s and c.comment_id=%s", (user_id,comment_id,))
                    post_likes = cursor.fetchall()
                    if post_likes:
                        print("\n this comment like is removed ")
                        cursor.execute("DELETE FROM Commentlikes WHERE comment_id =%s", (comment_id,))
                        cursor.execute("DELETE FROM Comments WHERE comment_id =%s", (comment_id,))
                        conn.commit()
                    else:
                        print("incorrect an comment_id ")
                another_action = input("\nDo you want to uncomment this (yes/no)? ").strip().lower()
            
        if command == "5":
            cursor.execute("SELECT cl.comment_id, cl.user_id, c.comment_text FROM Commentlikes cl INNER JOIN Comments c ON cl.comment_id = c.comment_id WHERE cl.user_id = %s", (user_id,))
            comment_likes = cursor.fetchall()
            if comment_likes:
                print("\nComments liked by you:")
                for like in comment_likes:
                    comment_id, like_user_id, comment_text= like
                    print(f"Comment ID: {comment_id} , Comment text: {comment_text}")
            
            another_action = input("\nDo you want to unlike this comment (yes/no)? ").strip().lower()
            while another_action == 'yes':
                comment_id=input("Enter comment_id ").strip()
                if comment_id :
                    cursor.execute("SELECT cl.comment_id FROM Commentlikes cl INNER JOIN Comments c ON cl.comment_id = c.comment_id WHERE cl.user_id = %s and c.comment_id=%s", (user_id,comment_id,))
                    post_likes = cursor.fetchall()
                    if post_likes:
                        print("\n this comment like is removed ")
                        cursor.execute("DELETE FROM Commentlikes WHERE comment_id =%s", (comment_id,))
                        conn.commit()
                    else:
                        print("incorrect an comment_id ")
                another_action = input("\nDo you want to unlike this comment (yes/no)? ").strip().lower()
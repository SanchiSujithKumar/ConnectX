create database facebookdb;
\c  facebookdb;

CREATE TABLE user_tb
(
  user_id INT NOT NULL,
  F_name VARCHAR(50),
  l_name VARCHAR(50),
  passwd VARCHAR(15),
  email VARCHAR(50),
  DOB DATE NOT NULL,
  phone bigint,
  PRIMARY KEY (user_id)
);

CREATE TABLE Posts
(
  post_id SERIAL PRIMARY KEY,
  post_content VARCHAR(256),
  post_Date DATE NOT NULL,
  user_id INT NOT NULL,
  post_likes INT NOT NULL DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES user_tb(user_id)
);

CREATE TABLE Friend
(
  Friend_id INT NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (Friend_id,user_id),
  FOREIGN KEY (user_id) REFERENCES user_tb(user_id),
  FOREIGN KEY (Friend_id) REFERENCES user_tb(user_id)
);

CREATE TABLE Posts_likes
(
  post_id INT NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (post_id, user_id),
  FOREIGN KEY (post_id) REFERENCES Posts(post_id),
  FOREIGN KEY (user_id) REFERENCES user_tb(user_id)
);

CREATE TABLE Photos
(
  photo_id SERIAL PRIMARY KEY,
  image_content VARCHAR(256),
  post_id INT NOT NULL,
  FOREIGN KEY (post_id) REFERENCES Posts(post_id)
);

CREATE TABLE shares
(
  post_id INT NOT NULL,
  user_id INT NOT NULL,
  count INT NOT NULL DEFAULT 1,
  FOREIGN KEY (post_id) REFERENCES Posts(post_id),
  FOREIGN KEY (user_id) REFERENCES user_tb(user_id)
);

CREATE TABLE Comments
(
  comment_id SERIAL PRIMARY KEY,
  commentdate DATE NOT NULL,
  post_id INT NOT NULL,
  user_id INT NOT NULL,
  comment_text VARCHAR(256) NOT NULL, 
  FOREIGN KEY (post_id) REFERENCES Posts(post_id),
  FOREIGN KEY (user_id) REFERENCES user_tb(user_id)
);

CREATE TABLE Commentlikes
(
  comment_id INT NOT NULL,
  user_id INT NOT NULL,
  FOREIGN KEY (comment_id) REFERENCES Comments(comment_id),
  FOREIGN KEY (user_id) REFERENCES user_tb(user_id)
);

CREATE TABLE Pages
(
  page_id SERIAL PRIMARY KEY,
  page_name VARCHAR(50) NOT NULL,
  DOC DATE, 
  createdBy INT NOT NULL,
  email varchar(50),
  page_content VARCHAR(10000),
  totalLikes int,
  foreign key (createdBy) references user_tb(user_id)
);

CREATE TABLE Page_likes
(
  user_id INT NOT NULL,
  page_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user_tb(user_id),
  FOREIGN KEY (page_id) REFERENCES Pages(page_id)
);


\i populate-data.sql
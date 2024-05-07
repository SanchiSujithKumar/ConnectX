INSERT INTO user_tb  VALUES('101', 'Revanth', 'Palaparthi', 1, '101@gmail.com', '2003-06-11', '9897364567');
INSERT INTO user_tb  VALUES('102', 'Sahitya', 'Chinta', 2, '102@gmail.com', '2003-11-30', '8125566123');
INSERT INTO user_tb  VALUES('103', 'Sanchi', 'Sujith', 3, '103@gmail.com', '2004-05-13', '9897367777');
INSERT INTO user_tb  VALUES('104', 'Pilli', 'Hamsini', 4, '104@gmail.com', '2004-08-22', '9897364222');
INSERT INTO user_tb  VALUES('105', 'Duddu', 'Hiday', 5, '105@gmail.com', '2004-01-04', '9897364676');

INSERT INTO Posts VALUES('10001', 'MY Memories', '2023-06-11', '101',2);
INSERT INTO Posts VALUES('10002', 'MY Memories', '2022-06-11', '101',2);
INSERT INTO Posts VALUES('10003', 'MY Memories', '2023-11-30', '102',2);
INSERT INTO Posts VALUES('10004', 'MY Memories', '2022-11-30', '102',2);
INSERT INTO Posts VALUES('10005', 'MY Memories', '2023-05-13', '103',2);
INSERT INTO Posts VALUES('10006', 'MY Memories', '2022-05-13', '103',0);
INSERT INTO Posts VALUES('10007', 'MY Memories', '2023-08-22', '104',2);
INSERT INTO Posts VALUES('10008', 'MY Memories', '2022-08-22', '104',0);
INSERT INTO Posts VALUES('10009', 'MY Memories', '2023-01-04', '105',2);
INSERT INTO Posts VALUES('10010', 'MY Memories', '2022-01-04', '105',1);
INSERT INTO Posts VALUES('10011', 'MY Memories', '2021-01-04', '105',0);

INSERT INTO Friend VALUES('102', '101');
INSERT INTO Friend VALUES('101', '102');
INSERT INTO Friend VALUES('104', '103');
INSERT INTO Friend VALUES('103', '104');
INSERT INTO Friend VALUES('102', '104');
INSERT INTO Friend VALUES('104', '102');
INSERT INTO Friend VALUES('105', '101');
INSERT INTO Friend VALUES('101', '105');
INSERT INTO Friend VALUES('103', '105');
INSERT INTO Friend VALUES('105', '103');

INSERT INTO Posts_likes VALUES('10001', '101');
INSERT INTO Posts_likes VALUES('10001', '102');
INSERT INTO Posts_likes VALUES('10002', '101');
INSERT INTO Posts_likes VALUES('10002', '102');
INSERT INTO Posts_likes VALUES('10003', '101');
INSERT INTO Posts_likes VALUES('10003', '102');
INSERT INTO Posts_likes VALUES('10004', '101');
INSERT INTO Posts_likes VALUES('10004', '102');
INSERT INTO Posts_likes VALUES('10005', '104');
INSERT INTO Posts_likes VALUES('10005', '103');
INSERT INTO Posts_likes VALUES('10007', '103');
INSERT INTO Posts_likes VALUES('10007', '104');
INSERT INTO Posts_likes VALUES('10009', '101');
INSERT INTO Posts_likes VALUES('10009', '103');
INSERT INTO Posts_likes VALUES('10010', '105');

INSERT INTO Photos VALUES('1001', 'cricket','10001');
INSERT INTO Photos VALUES('1002', 'king kohli','10002');
INSERT INTO Photos VALUES('1003', 'my family','10004');
INSERT INTO Photos VALUES('1004', 'keeravani','10005');
INSERT INTO Photos VALUES('1005', 'collegelife','10011');

INSERT INTO shares VALUES('10001', '102', 1);
INSERT INTO shares VALUES('10009', '103', 1);
INSERT INTO shares VALUES('10005', '104', 1);

INSERT INTO Comments VALUES(1,'2023-06-11','10001','102','C1');
INSERT INTO Comments VALUES(2,'2023-08-23','10007','103','C2');
INSERT INTO Comments VALUES(3,'2023-01-04','10011','101','C3');

INSERT INTO Commentlikes VALUES('01','102');
INSERT INTO Commentlikes VALUES('02','103');
INSERT INTO Commentlikes VALUES('03','101');
INSERT INTO Commentlikes VALUES('02','101');

INSERT INTO Pages VALUES('001','girls_page','2023-10-26',101,'101@gmail.com','This page is only for girls',1);
INSERT INTO Pages VALUES('002','boys_page','2023-10-26',102,'102@gmail.com','This page is only for boys',2);

INSERT INTO Page_likes VALUES('102','001');
INSERT INTO Page_likes VALUES('105','002');
INSERT INTO Page_likes VALUES('103','002');
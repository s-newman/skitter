CREATE DATABASE users;
USE users;

--- Create USER_INFO Table
CREATE TABLE USER_INFO (
    user_id int NOT NULL,
    username varchar(20) NOT NULL,
    first_name varchar(15),
    last_name varchar(25),
    email varchar(254) NOT NULL,
    session_id varchar(40),
    private_account bool,
    profile_picture_id int NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (profile_picture_id) REFERENCES PROFILE_PICTURE(picture_id)
);

--- Create PROFILE_PICTURE Table
CREATE TABLE PROFILE_PICTURE (
    picture_id int NOT NULL,
    picture varbinary(max) NOT NULL,
    PRIMARY KEY (picture_id)
);

--- Create FOLLOW Table
CREATE TABLE FOLLOW (
    follow_id int NOT NULL,
    follower_user_id NOT NULL,
    following_user_id NOT NULL,
    PRIMARY KEY (follow_id),
    FOREIGN KEY (follower_user_id) REFERENCES USER_INFO(user_id),
    FOREIGN KEY (following_user_id) REFERENCES USER_INFO(user_id)
);

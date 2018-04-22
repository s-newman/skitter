CREATE DATABASE IF NOT EXISTS users;
USE users;
-- GRANT ALL ON users.* to 'api-gateway'@'%';

-- Create PROFILE_PICTURE Table

CREATE TABLE PROFILE_PICTURE (
    picture_id int NOT NULL,
    picture varbinary(65500) NOT NULL,
    PRIMARY KEY (picture_id)
);

INSERT INTO PROFILE_PICTURE (picture_id, picture) VALUES (0, 0x41414141);

-- Create USER_INFO Table

CREATE TABLE USER_INFO (
    username varchar(15) NOT NULL,
    rit_username varchar(7) NOT NULL,
    first_name varchar(15),
    last_name varchar(25),
    email varchar(254) NOT NULL,
    private_account bool,
    profile_picture_id int NOT NULL,
    PRIMARY KEY (rit_username),
    FOREIGN KEY (profile_picture_id) REFERENCES PROFILE_PICTURE(picture_id)
);

-- Create FOLLOW Table

CREATE TABLE FOLLOW (
    follow_id int NOT NULL,
    follower_user_id varchar(7) NOT NULL,
    following_user_id varchar(7) NOT NULL,
    PRIMARY KEY (follow_id),
    FOREIGN KEY (follower_user_id) REFERENCES USER_INFO(rit_username),
    FOREIGN KEY (following_user_id) REFERENCES USER_INFO(rit_username)
);

-- Create SESSION Table

CREATE TABLE SESSION (
    rit_username varchar(7) NOT NULL,
    session_id varchar(80),
    PRIMARY KEY (rit_username)
);

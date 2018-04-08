CREATE DATABASE users;
USE users;
GRANT ALL ON users.* to 'api-gateway'@'%';

-- Create PROFILE_PICTURE Table

CREATE TABLE PROFILE_PICTURE (
    picture_id int NOT NULL,
    picture varchar(50) NOT NULL,
    PRIMARY KEY (picture_id)
);

-- Create USER_INFO Table

CREATE TABLE USER_INFO (
    rit_username varchar(7) NOT NULL UNIQUE,
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
    follower_user_id varchar(7) NOT NULL,
    following_user_id varchar(7) NOT NULL,
    PRIMARY KEY (follower_user_id, following_user_id),
    FOREIGN KEY (follower_user_id) REFERENCES USER_INFO(rit_username),
    FOREIGN KEY (following_user_id) REFERENCES USER_INFO(rit_username)
);

-- Create SESSION Table

CREATE TABLE SESSION (
    rit_username varchar(7) NOT NULL,
    session_id varchar(80) NOT NULL,
    PRIMARY KEY (rit_username)
);

-- Add default profile picture
INSERT INTO PROFILE_PICTURE (picture_id, picture) VALUES (
    0,
    '/static/img/default-profile.png'
);

-- Log queries
SET GLOBAL general_log=1;

-- Add users
DROP PROCEDURE IF EXISTS makeuser();
DELIMITER //
CREATE PROCEDURE makeuser()
BEGIN
    DECLARE start INT DEFAULT 0;
    WHILE start <= 999 DO:
        INSERT INTO USER_INFO (rit_username, first_name, last_name, email, profile_picture_id)
        VALUES (concat('test', start), 'Test', 'User', concat('test', start, '@rit.edu'), 0);
        SET start = start +1;
    END WHILE;
END //
DELIMITER ;
CALL PROCEDURE makeuser;
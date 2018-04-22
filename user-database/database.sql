CREATE DATABASE users;
USE users;
GRANT ALL ON users.* to 'api-gateway'@'%';

-- Create PROFILE_PICTURE Table

CREATE TABLE PROFILE_PICTURE (
    picture_id int NOT NULL AUTO_INCREMENT,
    picture varchar(50) NOT NULL,
    PRIMARY KEY (picture_id)
);

-- Create USER_INFO Table

CREATE TABLE USER_INFO (
    rit_username varchar(7) NOT NULL UNIQUE,
    first_name varchar(15),
    last_name varchar(25),
    email varchar(254) NOT NULL,
    session_id varchar(40),
    private_account bool,
    profile_picture_id int NOT NULL,
    PRIMARY KEY (rit_username),
    FOREIGN KEY (profile_picture_id) REFERENCES PROFILE_PICTURE(picture_id)
);

-- Create FOLLOW Table

CREATE TABLE FOLLOW (
    follower varchar(7) NOT NULL,
    followed varchar(7) NOT NULL,
    PRIMARY KEY (follower, followed),
    FOREIGN KEY (follower) REFERENCES USER_INFO(rit_username),
    FOREIGN KEY (followed) REFERENCES USER_INFO(rit_username)
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
    '/img/default-profile.png'
);

-- Log queries
SET GLOBAL general_log=1;

-- Add users
DELIMITER //
CREATE PROCEDURE makeuser()
BEGIN
    DECLARE start INT DEFAULT 0;
    WHILE start <= 999 DO
        INSERT INTO USER_INFO (rit_username, first_name, last_name, email, profile_picture_id) VALUES (
            concat('test', start),
            'Test',
            'User',
            concat('test', start, '@rit.edu'),
            0
        );
        SET start = start +1;
    END WHILE;
END//
DELIMITER ;
CALL makeuser;
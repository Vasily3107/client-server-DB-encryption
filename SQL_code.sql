CREATE DATABASE test_db;
USE test_db;


CREATE TABLE users (
--  column:             type:                    constraints:
    username            VARCHAR(256)             PRIMARY KEY,
    [password]          VARBINARY(256)           NOT NULL,
    last_online         DATETIME                 NOT NULL
);


CREATE TABLE decryption_data (
--  column:             type:                    constraints:
    username            VARCHAR(256)             FOREIGN KEY REFERENCES users(username),
    aes_key             VARBINARY(256)           NOT NULL,
    nonce               VARBINARY(256)           NOT NULL
);
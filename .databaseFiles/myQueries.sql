-- database: database.db
CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, devtag TEXT NOT NULL UNIQUE, password TEXT NOT NULL);

-- INSERT INTO id7-tusers(username,password) VALUES ("","");

--INSERT INTO users(devtag,password) VALUES ("max","password");

-- SELECT * FROM extension;

ALTER TABLE users ADD COLUMN email TEXT NOT NULL;

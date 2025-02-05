--database: database.db
--CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, devtag TEXT NOT NULL UNIQUE, password TEXT NOT NULL);

--CREATE TABLE entries(devtag TEXT NOT NULL, project TEXT NOT NULL, repo TEXT NOT NULL, starttime TEXT NOT NULL, endtime TEXT NOT NULL)
--DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    devtag TEXT NOT NULL,
    project TEXT NOT NULL,
    repo TEXT NOT NULL,
    starttime TEXT NOT NULL,
    endtime TEXT NOT NULL
);
--CREATE TABLE entries(devtag TEXT NOT NULL, project TEXT NOT NULL, starttime TEXT NOT NULL, endtime TEXT NOT NULL)
-- INSERT INTO id7-tusers(username,password) VALUES ("","");

--INSERT INTO users(devtag,password) VALUES ("max","password");

-- SELECT * FROM extension;
CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    devtag TEXT NOT NULL,
    project TEXT NOT NULL,
    repo TEXT NOT NULL,
    starttime TEXT NOT NULL,
    endtime TEXT NOT NULL
);
INSERT INTO entries(devtag,project,repo,starttime,endtime) VALUES ("max","project","repo","starttime","endtime");
PRAGMA foreign_keys=on;

CREATE TABLE clients(
 id INTEGER PRIMARY KEY,
 login TEXT NOT NULL,
 information TEXT NOT NULL
);

CREATE TABLE logs(
id INTEGER PRIMARY KEY,
client_id INTEGER NOT NULL,
activity INTEGER NOT NULL,
ip TEXT NOT NULL,
FOREIGN KEY (client_id) REFERENCES clients(id)
 );

CREATE TABLE list_contacts(
id INTEGER PRIMARY KEY,
client_id INTEGER NOT NULL,
list TEXT NOT NULL,
FOREIGN KEY (client_id) REFERENCES clients(id)
);
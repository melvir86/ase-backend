DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS card;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS car;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TABLE card (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name TEXT NOT NULL,
  number TEXT NOT NULL,
  expiry_month TEXT NOT NULL,
  expiry_year TEXT NOT NULL,
  cve TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  description TEXT NOT NULL,
  feedback TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE booking (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  car_id INTEGER NULL,
  created TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  source TEXT NOT NULL,
  destination TEXT NOT NULL,
  cost TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
  FOREIGN KEY (car_id) REFERENCES car (id)
);

CREATE TABLE car (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  brand TEXT NOT NULL,
  model TEXT NOT NULL,
  colour TEXT NOT NULL,
  next_service TEXT NOT NULL,
  status TEXT NOT NULL,
  pos_x INTEGER,
  pos_y INTEGER,
  rating TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Preparing sample data before we develop the feature

INSERT INTO user (username, password, role) VALUES ('DriverJohn', '42f749ade7f9e195bf475f37a44cafcb', 'Driver');

INSERT INTO user (username, password, role) VALUES ('DriverRobert', '42f749ade7f9e195bf475f37a44cafcb', 'Driver');

INSERT INTO user (username, password, role) VALUES ('Mary', '42f749ade7f9e195bf475f37a44cafcb', 'Customer');

INSERT INTO user (username, password, role) VALUES ('Johnny', '42f749ade7f9e195bf475f37a44cafcb', 'Customer');

INSERT INTO user (username, password, role) VALUES ('Alan', '42f749ade7f9e195bf475f37a44cafcb', 'Provider');

INSERT INTO car (user_id, brand, model, colour, next_service, status,pos_x,pos_y,rating) VALUES (1, 'Mazda', '3 Hb', 'Red', '23/06/2023', 'Active','50','42',8);

INSERT INTO car (user_id, brand, model, colour, next_service, status,pos_x,pos_y,rating) VALUES (2, 'Mazda', '6', 'Blue', '23/12/2023', 'Active','42','54',7);

INSERT INTO booking (user_id, source, destination, cost, status) VALUES (3, 'Wembley Park', 'Euston Square', '$10.50', 'Booked');

INSERT INTO booking (user_id, source, destination, cost, status) VALUES (3, 'Picadilly Circus', 'Goodge Street', '$7.50', 'Booked');
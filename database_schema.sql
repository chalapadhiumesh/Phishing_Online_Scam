
CREATE TABLE app_users (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	username VARCHAR(50) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	`role` ENUM('USER','ADMIN') NOT NULL, 
	created_at DATETIME DEFAULT now(), 
	is_active BOOL, 
	PRIMARY KEY (id)
)

;


CREATE TABLE app_url_scans (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	url TEXT NOT NULL, 
	prediction VARCHAR(20) NOT NULL, 
	confidence FLOAT NOT NULL, 
	risk_score INTEGER NOT NULL, 
	risk_level VARCHAR(20) NOT NULL, 
	indicators TEXT, 
	timestamp DATETIME DEFAULT now(), 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES app_users (id)
)

;


CREATE TABLE app_message_scans (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	message_text TEXT NOT NULL, 
	prediction VARCHAR(20) NOT NULL, 
	confidence FLOAT NOT NULL, 
	risk_score INTEGER NOT NULL, 
	risk_level VARCHAR(20) NOT NULL, 
	indicators TEXT, 
	timestamp DATETIME DEFAULT now(), 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES app_users (id)
)

;


CREATE TABLE app_feedback (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	scan_type VARCHAR(20) NOT NULL, 
	scan_id INTEGER NOT NULL, 
	is_accurate BOOL NOT NULL, 
	comments TEXT, 
	timestamp DATETIME DEFAULT now(), 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES app_users (id)
)

;


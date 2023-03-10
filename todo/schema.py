instructions = [
	'SET FOREIGN_KEY_CHECKS=0',
	'DROP TABLE IF EXISTS todo',
	'DROP TABLE IF EXISTS user',
	'SET FOREIGN_KEY_CHECKS=1',
	"""
		CREATE TABLE users (
			id INT PRIMARY KEY AUTO_INCREMENT,
			username VARCHAR(50) UNIQUE NOT NULL,
			password VARCHAR(100) NOT NULL
		);
	""",
	"""
		CREATE TABLE todo (
			id INT PRIMARY KEY AUTO_INCREMENT,
			created_by INT NOT NULL,
			created_ad TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			description TEXT NOT NULL,
			completed BOOLEAN NOT NULL,
			FOREIGN KEY(created_by) REFERENCES users(id)
		);
	"""
]

# alter table users modify column password varchar(150) not null
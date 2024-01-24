DROP TABLE IF EXISTS Documents;
CREATE TABLE Documents( 
	doc_name varchar(45),
	owner varchar(45),
	FOREIGN KEY (owner) REFERENCES Users(username),
	PRIMARY KEY (owner, doc_name)
);

CREATE TABLE User (
        id INTEGER NOT NULL, 
        username VARCHAR(20) NOT NULL,   
        email VARCHAR(120) NOT NULL,     
        image_file VARCHAR(20) NOT NULL, 
        password VARCHAR(60) NOT NULL,
        last_seen DATE,
        is_admin BOOLEAN, 
        is_manager BOOLEAN,
        is_active BOOLEAN,
        PRIMARY KEY (id),
        UNIQUE (username),
        UNIQUE (email),
        CHECK (is_admin IN (0, 1)),      
        CHECK (is_manager IN (0, 1)),    
        CHECK (is_active IN (0, 1))      
);
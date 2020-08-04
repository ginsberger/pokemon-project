USE pokemon_project;

DROP TABLE OwnedBy;
DROP TABLE Pokemon_Type;
DROP TABLE Pokemon;
DROP TABLE Type_;
DROP TABLE Trainer;

CREATE TABLE Type_(
    id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(20) NOT NULL UNIQUE
);


CREATE TABLE Pokemon(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_ VARCHAR(20),
    height INT,
    weight_ INT
);


CREATE TABLE Pokemon_Type(
    type_id INT,
    pokemon_id INT,
    PRIMARY KEY(type_id, pokemon_id),
    FOREIGN KEY(type_id) REFERENCES Type_(id),
    FOREIGN KEY(pokemon_id) REFERENCES Pokemon(id)
);


CREATE TABLE Trainer(
    name_ VARCHAR(20) PRIMARY KEY,
    town VARCHAR(20)
);


CREATE TABLE OwnedBy(
    pokemon_id INT,
    pokemon_name VARCHAR(20),
    trainer_name VARCHAR(20),
    PRIMARY KEY(pokemon_name, trainer_name),
    FOREIGN KEY(pokemon_id) REFERENCES Pokemon(id),
    FOREIGN KEY(trainer_name) REFERENCES Trainer(name_)
);

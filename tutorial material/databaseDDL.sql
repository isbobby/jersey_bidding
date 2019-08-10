/*
    A single table for each sport will be created for each sport, a separate dict will be created to
    loop through all the sports and inputting the entries in a CSV file (combined.csv). The entires 
    in combined.csv are then updated and stored in CombinedList for front end use. 

    Another table NameList records the personal details that are not vital but useful.

    ON DELETE CASCADE allows cascading delete

    CREATE TABLE <table_name> ( attribute_name attribute_type attribute_conditions ); creates table
    CONSTRAINT keyword defines the primary key for each table
*/

CREATE TABLE BasketballMembers (
    RoomNumber char(25) NOT NULL,
    Captaincy boolean NOT NULL,
    IVP boolean NOT NULL,
    IHGYears integer NOT NULL,
    
    CONSTRAINT BasketballMembersPK PRIMARY KEY(RoomNumber)
);

CREATE TABLE CombinedList (
    RoomNumber char(25) NOT NULL,
    BiddingPoints integer NOT NULL

    CONSTRAINT CombinedListPK PRIMARY KEY(RoomNumber)
);

CREATE TABLE NameList (
    UserID integer NOT NULL,
    UserName char(50) NOT NULL,
    ShirtSize char(5) NOT NULL,
    RoomNumber char(25) NOT NULL,

    CONSTRAINT NameListPK PRIMARY KEY(UserID)
    CONSTRAINT RoomNumberFK FOREIGN KEY(RoomNumber) REFERENCES CombinedList(RoomNumber) ON DELETE CASCADE
)

/*
    This part contains the documentation of ALTER statements, alter statements
    are used to modify the constraints or add new constraints to a relation.
*/

ALTER TABLE NameList 
    ADD CONSTRAINT NameListPK PRIMARY KEY(UserID, RoomNumber)
    ADD CONSTRAINT RoomNumberFK FOREIGN KEY(RoomNumber) REFERENCES CombinedList(RoomNumber) ON DELETE CASCADE
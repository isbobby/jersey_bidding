/*
    This file records the SQL used to manipulate data to perform insert,
    update and delete operations

    INSERT syntax - to add a new row populated with values:

        INSERT INTO <table name> (stringattribute, integerattribute, booleanattribute )
            VALUES ('String values', 25, True )

        Values are in order
        Non-numeric values should be in single quotes (')


    UPDATE syntax - to change the values in exisitng rows:

        UPDATE <table name>
        SET attribute = new_value
        WHERE primary_key = pk

        *This changes the entire table
        UPDATE <table name>
        SET attribute = new_value 

        DELETE syntax 

        DELETE FROM <table name> WHERE primary_key = pk

        *This deletes the entire table
        DELETE FROM <table name>

    SELECT syntax - Query 

        SELECT <one or more attributes> 
        FROM <table name>
        WHERE primary_key = pk

        SELECT DISTINCT <one or more attributes>
        FROM <table name>
        WHERE primary_key = pk

        Powerful keywords under WHERE clause 
        *DISTINCT keyword results in the database only displaying distinct elements
        
        *The WHERE clause establish conditions, WHERE clause also allows logical operators
            *NOT operator is able to negate the conditions
            *BETWEEN operator is able to represent range: WHERE age BETWEEN 10 AND 45 (inclusive range)
        
        *LIKE enables partial searches and can be paired with wildcard characters:
            -The multiple character is represented by (%) 
                -WHERE name LIKE 'Da%' queries all names begining with DA
            -The single character is represented by (_)
                -WHERE phone LIKE '8181 ____';
        
        *ORDER to sort data
            ORDER BY age ASC; => sort by ascending (default)
            ORDER BY age DESC; => sort by descending 
        
        *COUNT 
            counts the number of rows that meet the specific criteria 
        
        *MIN/MAX 
            Finds the min/max value for specific column

*/ 

INSERT INTO BasketballMembers (RoomNumber, Captaincy, IVP, IHGYears ) 
    VALUES ('A110', True, True, 3);

UPDATE BasketballMembers
SET IHGYears = 2
WHERE RoomNumber = 'A110'

DELETE FROM BasketballMembers WHERE RoomNumber = 'A110'

SELECT IHGYears 
FROM BasketballMembers
WHERE RoomNumber = 'A110'

SELECT Example
FROM Test
WHERE condition IN (4, 8, 9)
/* Equivalent to */
WHERE condition = 4 OR condition = 8 OR condition = 9

/* counts the number of employees */
SELECT COUNT (*)
FROM employee 

/* 
    displays the stats for the a specific group of employees
    aliases are used by using AS keyword
 */
SELECT MIN(hours) AS minHours,
       MAX(hours) AS maxHours,
       AVG(hours) AS avhHours,
FROM employee 
WHERE (age BETWEEN 10 AND 45) AND (phone LIKE '8181____')

/*
    Subqueries

    noncorrelated: the inner query only has to run once in order for the
    database engine to complete search 

    correlated: thje inner query's search condition depends on the result
    from the outer query
*/

SELECT empname
FROM Employee 
WHERE deptID IN 
    (
    SELECT deptID
    FROM Department
    WHERE deptName LIKE 'tech%'
    )

/*
    1.DB Scans Employee, sees the employee's dept ID = 5
    2.Inner query search through dept ID = 5 and computes average salary
    3.Outer query compares and select the empname that fits the condition
*/
SELECT empname
FROM Employee e
WHERE empSalary > (
    SELECT AVG(empSalary)
    FROM Employee
    WHERE deptID = e.deptID
);

/*
    JOIN keyword
*/
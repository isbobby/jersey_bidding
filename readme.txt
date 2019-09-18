A rough description of the development plan of Jerseybidding.com

#Phases of development  
    1. Program flow chart, database models and overall project ideation (week 1)
    2. Prototype development using Flask, embedded with HTML, CSS and JS (week 2-3)
    3. Fomulating test cases and product testing (week 3)
    4. Production and server allocation (week 4)
    5. User testing and feedback, debugging (week 5)
    6. Actual deployment (week 7-8, early october)

#Brief description on product agenda
Jersey bidding is similar to any other bidding process. Each user will be allocated points 
that depend on years of IHG participation, captaincy and invovement in IVP. The aim of this
web application is to automate point calculation, verificaiton of points, sorting of users
according to points and allocating a number base on user choice and the points they have.

    #Points formular (tentative, non-inclusive of all corner cases)
    Total points = ( IHG Years * 100 ) + ( number of sports * 1 ) + 2 (if captaincy == True ) + 2 (if IVP == True )

    #UX
    1. Real time bidding system
    Users will be able to select a desired number on the website, currently each user can 
    only choose a single number to bid for

    if user is the highest bidder
        app displays: you are currently the highest bidder
    else if user is not the highest bidder
        app displays: you are outbidded, the highest bidder has x points, you have y points
    
    2. Real time update
    Users will receive notifications if they are outbidded by another user with higher points
    via email/telegram notifications (Plausible via APIs but difficult to implement)

    Alternatively, Eusoffworks can be engaged to display the number status in dining hall.

#Database model

#Execution plan
    1. Retrieve lists in CSV files from all sports, non-participants are to be grouped in a 
    different list with 0 points (lowerest prioity)

    2. Create table for each sport

    3. Loop through the tables to calculate points (achieving point calculation and verificaiton)

    4. Upload new entries in a combined list 
    
    5. Deploy website for users to bid. Each user entry in the combined list contains the points 
    they have post-calculation



SMC
-Web page phrasing
-Distribute password
-fill up the template 

Us
-Close down temporarily at 9pm to deconflict (sun)

-remove check result (route)

-remove email (boon)

-show points n choices under admin page (tonight)

-rename excel year column to number of ihg (tonight)

-allocate by year correction

-0 to 3+ years (boon urgent)

-EDIT UI
-reminder for admin to reduce error (tonight b)

-username loading and password (tonight)
# tell them not to change the order
1. generate username password
2. give back pw file to smc 
3. give smc input in the same order
4. approve output.csv
5. take back full input to setupsql
6. format


1. Take namelist from AMOS
2. generate PW by hackers
3. SMC Distribute password
4. 
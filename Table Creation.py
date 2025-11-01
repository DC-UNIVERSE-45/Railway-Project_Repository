#                                            TABLE CREATION PAGE

import mysql.connector as sq

mydb = sq.connect(host="localhost", user="root", passwd="Debjit@08#2025")
cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Railway_Reservation_System")
cursor.execute("USE Railway_Reservation_System")

#________________________________________________________________________________________________________
# TABLE: TRAIN
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Train(
        Tno INT NOT NULL PRIMARY KEY,
        Tname VARCHAR(45),
        Source VARCHAR(45),
        Destination VARCHAR(45),
        Halt VARCHAR(45),
        Fare INT
    )
""")

#________________________________________________________________________________________________________
# TABLE: BOOKING
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Booking(
        Pnr INT NOT NULL PRIMARY KEY, 
        Tno INT NOT NULL,
        Jdate DATE NOT NULL,
        Source VARCHAR(45),
        Destination VARCHAR(45),
        NoofPassenger INT,
        Amount int,
        FOREIGN KEY (Tno) REFERENCES Train(Tno)
    )
""")

#________________________________________________________________________________________________________
# TABLE: CANCELLATION
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cancellation(
        Pnr INT,
        Amount INT,
        Refund INT,
        FOREIGN KEY (Pnr) REFERENCES Booking(Pnr)
    )
""")

#________________________________________________________________________________________________________
# TABLE: USERS
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users(
        UID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(45),
        Age INT,
        DOB DATE,  
        Gender ENUM('Male', 'Female', 'Other') NOT NULL,
        State VARCHAR(100) NOT NULL,
        Password VARCHAR(255) NOT NULL
    )
""")

print("✅ All tables created successfully!")

mydb.close()

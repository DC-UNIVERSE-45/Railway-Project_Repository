#                                            TABLE CREATION PAGE

import mysql.connector as sq
mydb = sq.connect(host="localhost", user="root", passwd="Debjit@08#2025")
cursor = mydb.cursor()
cursor.execute("create database if not exists Railway_Reservation_System")
cursor.execute("use Railway_Reservation_System")
#________________________________________________________________________________________________________
# TABLE CREATION TRAIN
cursor.execute("""
               create table if not exists Train(
                    Tno int not null primary key,
                    Tname varchar(45),
                    Source varchar(45),
                    Destination varchar(45),
                    Halt varchar(45)
               )
""")
#________________________________________________________________________________________________________
# TABLE CREATION PASSENGER
cursor.execute("""
               create table if not exists PASSENGER(
                    Aadhar_no int not null primary key,
                    Tno int not null,
                    Pname varchar(45),
                    SEX varchar(45),
                    Address varchar(45),
                    foreign key (Tno) references Train(Tno)
               )
""")
#________________________________________________________________________________________________________
# TABLE CREATION Booking
cursor.execute("""
               create table if not exists Booking(
                    Tno int not null,
                    Pnr int not null primary key, 
                    Jdate DATE not null,
                    Source varchar(45),
                    Destination varchar(45),
                    Aadhar_no int,
                    foreign key (Aadhar_no) references Passenger(Aadhar_no) 
               )
""")
#________________________________________________________________________________________________________
# TABLE CREATION Fare
cursor.execute("""
               create table if not exists Fare(
                    Tno int not null,
                    Pnr int,
                    Class int,
                    NoofPassenger int,
                    fare int,
                    amount int,
                    foreign key (Pnr) references Booking(Pnr) 
               )
""")
#________________________________________________________________________________________________________
# TABLE CREATION CANCELLATION
cursor.execute("""
               create table if not exists CANCELLATION(
                    Tno int not null,
                    Pnr int,
                    amount int,
                    refund int,
                    foreign key (Tno) references Train(Tno) 
               )
""")
#________________________________________________________________________________________________________
# TABLE CREATION USERS
cursor.execute("""
    CREATE TABLE IF NOT EXISTS USERS(
        UID INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(45),
        age INT,
        dob DATE,  
        gender ENUM('Male', 'Female', 'Other') NOT NULL,
        state VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
""")
#________________________________________________________________________________________________________
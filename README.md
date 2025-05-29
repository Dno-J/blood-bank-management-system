🩸 Blood Bank Management System
📖 Overview
The Blood Bank Management System is a desktop application developed using Python's Tkinter library for the GUI and MySQL for the backend database. It facilitates efficient management of blood donations and requests, ensuring streamlined operations for blood banks and hospitals.

🎯 Features
-Admin Authentication: Secure login system for administrators.
-Blood Inventory Management: Real-time tracking of blood units by blood group.
-Donation and Request Handling: Modules to record blood donations and requests with patient details.
-Transaction Records: Comprehensive logs of all donation and request activities.
-User-Friendly Interface: Intuitive GUI for seamless navigation and operation.

🛠️ Technologies Used
-Programming Language: Python
-GUI Library: Tkinter
-Database: MySQL
-Database Connector: mysql-connector-python

🗃️ Database Schema
The application utilizes the following database tables:

Admins:
-username: VARCHAR(50) - Primary Key
-password: VARCHAR(50)

BloodBank:
-Blood_Grp: VARCHAR(5) - Primary Key
-units: INT

Transactions:
-id: INT - Primary Key, Auto-increment
-name: VARCHAR(100)
-blood_grp: VARCHAR(5)
-units: INT
-action: VARCHAR(10)
-date: DATETIME
-gender: VARCHAR(10)
-contact_number: VARCHAR(15)

🚀 Getting Started
Prerequisites
Python 3.x
MySQL Server
mysql-connector-python package

🔨Installation
1.Clone the Repository:
bash:
git clone https://github.com/yourusername/blood-bank-management-system.git
cd blood-bank-management-system

2.Set Up the Database:
-Open MySQL Workbench or your preferred MySQL interface.
-Run the provided blood_bank_schema.sql script to create the necessary database and tables.

3.Configure Database Connection:
-In the Python script, locate the DB_CONFIG dictionary.
-Update the host, user, password, and database fields as per your MySQL configuration.
-python:
DB_CONFIG = {
    'host': "localhost",
    'user': "your_mysql_username",
    'password': "your_mysql_password",
    'database': "db"
}

4.Install Dependencies:
bash:
pip install mysql-connector-python

5.Run the Application:
bash:
python your_main_script.py

🤝 Contributing
Contributions are welcome! If you'd like to enhance the application or fix issues, please fork the repository and submit a pull request.

📄 License
This project is licensed under the MIT License.

📞 Contact
For any inquiries or support, please contact jacksondino00@gmail.com

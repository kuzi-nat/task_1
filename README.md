# Hostel Management System
This Python program is designed to manage a hostel's database. It connects to a MySQL database and performs various operations like creating the database, tables, inserting data, executing queries, and exporting results to JSON or XML files.

## Setup

### Prerequisites
- Python 3.x installed on your system.
- MySQL server installed and running.

### Installation
1. Clone this repository to your local machine.
2. Install the required Python packages by running:
 ```
   pip install -r requirements.txt
   ```
3. Create a .env file in the root directory and add the following environment variables:
```
   host=your_mysql_host
   user=your_mysql_username
   password=your_mysql_password
   db_name=your_database_name
   ```
## Usage
1. Run the program by executing python `main.py`.
2. Follow the prompts to enter the file paths for rooms and students data.
3. Choose the export file type (JSON or XML) when prompted.
4. Enter the desired file name for the export.

## Files
- `main.py`: Main Python script containing the program logic.
- queries.py: Module containing SQL queries used by the program.
- .env: Environment variables file storing MySQL connection details.

import json
import mysql.connector 
from mysql.connector import Error

password_path = "./sql_config/sql_password.json"
with open(password_path,'r') as json_file:
    password_dict = json.load(json_file)
password = password_dict['password']    

class MySql:
    def __init__(
                self,
                 password=password,
                 host='localhost',
                 user='root',
                 database='ml_email'
                 ) -> None:
        
        self.password = password
        self.host = host
        self.user = user
        self.database = database
        
    
    def create_db(self):
        """
        Create the database to store emails and inferences
        """
        try:
            conn = mysql.connector.connect(host=self.host,
                                                 user=self.user,
                                                 password=self.password)
            
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {self.database} DEFAULT CHARACTER SET 'utf8'")
            
            conn.database = self.database
            
            # create email table 
            email_table_query = """
                CREATE TABLE IF NOT EXISTS email (
                email_id INT AUTO_INCREMENT PRIMARY KEY,
                date DATETIME,
                sender VARCHAR(255),
                subject VARCHAR(1000),
                body VARCHAR(1000)
            )
            """
            cursor.execute(email_table_query)
            print("Table 'email' created successfully or already exists.")
            
             # Create inference table
            inference_table_query = """
            CREATE TABLE IF NOT EXISTS inference (
                inference_id INT AUTO_INCREMENT PRIMARY KEY,
                email_id INT,
                label VARCHAR(45),
                score DOUBLE,
                FOREIGN KEY (email_id) REFERENCES email(email_id)
            )
            """
            cursor.execute(inference_table_query)
            print("Table 'inference' created successfully or already exists.")
            print(f"Database {self.database} created successfully.")
            
        except mysql.connector.Error as err:
            print(f"Failed to create database {self.database}: {err}")
            exit(1)  
              
        finally:
            cursor.close()
            conn.close()
        
        
    def connect_to_db(self):
        """ Connect to the db 

        Returns:
            _type_: connection
        """
        self.connection = mysql.connector.connect( 
            host=self.host, 
            user=self.user,
            password=self.password,
            database=self.database
            )
        return self.connection
    
    
    def insert_data(self, email_data, inference_data):
        """Insert values in the database 

        Args:
            email_data (tuple): tuple with the different values related to email
            inference_data (tuple): tuple with the different values related to inference
        """        
        try:
            cursor = self.connection.cursor()
            
            insert_email_data = """
            INSERT INTO email (date, sender, subject, body)
            VALUES (%s, %s, %s, %s)
            """
            insert_inference_data = """
            INSERT INTO inference (email_id,label, score)
            VALUES (%s, %s, %s)
            """

            cursor.execute(insert_email_data, email_data)
            
            last_inserted_id = cursor.lastrowid
            inference = (last_inserted_id,) + inference_data
            
            cursor.execute(insert_inference_data, inference)
            
            self.connection.commit()
            print("Data inserted successfully into both tables")
            
        except Error as e:
            print(f"Error: {e}")
            if self.connection.is_connected():
                self.connection.rollback()
    
        finally:
            if self.connection.is_connected():
                cursor.close()
                self.connection.close()
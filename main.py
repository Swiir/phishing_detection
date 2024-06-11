import time
import signal
import threading
import gmail.google_api as gg
from mysql.connector import Error
import sql_config.sql_function as sc
from optimum.pipelines import pipeline
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer
import process_function as pf

model_path = "./models/onnx/"

stop_event = threading.Event()

def signal_handler(sig, frame):
    print("Stopping the application...")
    stop_event.set()
    
if __name__=="__main__":
    
    signal.signal(signal.SIGINT, signal_handler)
    # Build gmail service 
    service = gg.authenticate_gmail()
    db_connection = None
    previous_date = None

    # Load the model 
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = ORTModelForSequenceClassification.from_pretrained(model_path)
    onnx_qa = pipeline("text-classification", model=model, tokenizer=tokenizer, accelerator="ort", truncation=True)
      
    while not stop_event.is_set():
        try:
            # connect to the db 
            if db_connection is None or not db_connection.is_connected():
                my_sql = sc.MySql()
                db_connection = my_sql.connect_to_db()
                db_info = db_connection.get_server_info()
                print(f"Connected to MySQL Server version {db_info}")
            
            # Retrieve the email info
            email_data = gg.get_email_details(service)
            date = email_data['date']
            # convert date in datetime 
            converted_date = pf.Process().parse_date(date)
            sender = email_data['from']
            subject = email_data['subject']
            body = email_data['body']
            
            
            # Make the inference on the new email and store the data 
            if previous_date is None or date !=previous_date or sender != previous_sender or subject != previous_subject:
                print(f"Date: {date}")
                print(f"From: {sender}")
                print(f"Subject: {subject}")

                # create a file with the body of the mail 
                body_path = pf.Process().create_txt_file(body)
                
                # Concat the values into one 
                non_none_values = [str(value) for value in email_data.values() if value is not None]
                concat_email = ''.join(non_none_values)
                print(concat_email)
                # run inference
                inference = onnx_qa(concat_email)
                print("Model's inference:")
                print(inference)
                
                # Store the data into  the db 
                data_email = (converted_date, sender, subject, body_path)
                data_inference = (inference[0]['label'], inference[0]['score'])
                
                my_sql.insert_data(data_email, data_inference)
                
            previous_date = date
            previous_sender = sender
            previous_subject = subject
            previous_body = body
            
            time.sleep(60) 

        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

        finally:
            if db_connection.is_connected():
                db_connection.close()
                print("MySQL connection is closed")
                db_connection = None
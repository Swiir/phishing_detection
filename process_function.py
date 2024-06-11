from datetime import datetime
import os

class Process:

    def __init__(self, base_name="email_text", email_directory = "./data/email/") -> None:
        self.email_directory = email_directory
        self.base_name = base_name
        
        
    def parse_date(self, date_str:str) -> datetime:
        """ Convert date in string format to datetime format

        Args:
            date_str (str): Date in string format 

        Raises:
            ValueError: Error if the format of the date is not in the list of formats

        Returns:
            datetime: date in datetime format
        """
        formats = [
            '%a, %d %b %Y %H:%M:%S %z (%Z)',
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S %Z'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"time data '{date_str}' does not match any known format")
    
    
    def create_txt_file(self, data:str):
        """Create txt file to store the text data from the email

        Args:
            data (str): string data to store 
        Returns:
            str: path of the created file 
        """
        # init the counter 
        counter = 1
        
        while True:
            
            file_name = f"{self.base_name}_{counter}.txt"
            file_path = os.path.join(self.email_directory, file_name)
            if not os.path.exists(file_path):
                # create the file
                with open(file_path, 'w') as file:
                    file.write(data)
                    
                print(f"file created: {file_path}")
                break
            counter +=1
            
        return file_path
                
                
    
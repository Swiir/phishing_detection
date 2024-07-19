# Indesirable email detection  

## Summary  

This is a personal project and the goal is to practice and gain knowledge on the used of LLM models. 
For simplicity's sake and out of curiosity I developped everything in local. 
The idea here is to use the CEAS_08 dataset to fine tune the distilbert model to classify email.  
This model works only with email written in english because the dataset is in english.  
Find below the key point of this project:

- Prepare the dataset
- Fine tune Distilbert model with the dataset
- Connect to the Gmail API to retrieve email
- Make inference on email
- Store the email info and inferences in a SQL database  

For now there are no actions that are made after the inference but there is the possibility to put the email in a specified inbox with the gmail API.

## Setup

- follow the guide https://developers.google.com/gmail/api/quickstart/python?hl=en to setup the Gmail API
- download the CEAS_08 dataset and put it in the data folder if you want to fine tune the model https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset
- Install My SQL and configure it
- install the required packages with pip install -r requirements.txt
- Create the database by running the file create_db.py
- Run the script main.py to run the application

## Reference

Dataset:
*Al-Subaiey, A., Al-Thani, M., Alam, N. A., Antora, K. F., Khandakar, A., & Zaman, S. A. U. (2024, May 19). Novel Interpretable and Robust Web-based AI Platform for Phishing Email Detection. ArXiv.org. https://arxiv.org/abs/2405.11619*

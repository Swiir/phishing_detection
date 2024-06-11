import pandas as pd
import os
from datasets import Dataset, DatasetDict
import process_data_function as pf

# path 
raw_data_path = "../data/raw/CEAS_08.csv"
process_path = "../data/processed/"

# import the data 
df = pd.read_csv(raw_data_path)
print('The data has been succesfully imported')
print(f'Number of columns: {len(df.columns)}')
print(f'Number of record: {len(df)}')

# drop the unused column 
drop_df = df.drop(['receiver', 'urls'], axis=1)
print('-----------------------------------')
print('Succesfully removed unused columns')
print(f'Number of columns: {len(drop_df.columns)}')
print(f'Number of record: {len(drop_df)}')

# concatenate the strings into one string 
concat_df = pf.concatenate_str(drop_df)

# remove nan values 
concat_df = concat_df.dropna(axis=0)
print('-----------------------------------')
print('Succesfully removed None records')
print(f'Number of columns: {len(concat_df.columns)}')
print(f'Number of record: {len(concat_df)}')

# format the data into a dict
dataset_dict = pf.format_data(concat_df)

# convert in Dataset object 
dataset = DatasetDict({
    "train":Dataset.from_dict(dataset_dict["train"]),
    "test":Dataset.from_dict(dataset_dict["test"]),
    "val":Dataset.from_dict(dataset_dict["val"]),
})

# save the data
data_path = os.path.join(process_path, 'dataset')

dataset.save_to_disk(data_path)

print('-----------------------------------------')
print(f'Data has been saved succesfully in {process_path}')

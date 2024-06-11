import pandas as pd
from sklearn.model_selection import train_test_split

def concatenate_str(df:pd.DataFrame)-> pd.DataFrame:
    """ Concatenate str from a DataFrame.

    Args:
        df (pd.DataFrame): df with the str to concat 

    Returns:
        pd.DataFrame: df with the concat str 
    """
    columns = df.columns
    
    # filter columns 
    filtered_col = [col for col in columns if col !='label']
    # concat the str 
    df['concat'] = df[filtered_col[0]].str.cat(df[filtered_col[1:]], sep=' ')
    
    # remove useless columns
    new_df = df.drop(filtered_col, axis=1)
    
    return new_df 


def format_data(df:pd.DataFrame)->dict:
    """Format the data into a dict with a train, test set

    Args:
        df (pd.DataFrame): DataFrame with the data to format

    Returns:
        dict: Dataset with the train, test, val set
    """
    train, eval_ = train_test_split(df,
                                    test_size=0.3,
                                    random_state=19,
                                    stratify=df['label'])
    
    test, val = train_test_split(eval_,
                                 test_size=0.5,
                                 random_state=19,
                                 stratify=eval_['label'])
    
    data_set = {
        "train":{
            "text":train['concat'].to_list(),
            "label":train['label'].to_list()
            },
        "test":{
            "text":test['concat'].to_list(),
            "label":test['label'].to_list()
            },
        "val":{
            "text":val['concat'].to_list(),
            "label":val['label'].to_list()
        }
    }
    return data_set
        
    

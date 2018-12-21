import csv, redis, json
import pandas as pd
import ast

REDIS_HOST = 'localhost'
conn = redis.Redis(REDIS_HOST)

def store_data(csv_file_path):
    # Importing the training set
    dataset_train = pd.read_csv(csv_file_path)
    dataset_train = dataset_train[['SC_CODE', 'SC_NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE']]
    # dataset_train.set_index('SC_NAME', inplace=True)
    # dataset_train.head()

    pipe = conn.pipeline()
    for i in range(len(dataset_train)):
        # print(dataset_train.iloc[i][1], dataset_train.iloc[i].to_json())
        pipe.set(dataset_train.iloc[i][1], dataset_train.iloc[i].to_json())
    pipe.execute()
    print('done')


def get_data():
    keys = conn.scan(cursor=0, count=11)
    lis = []
    for key in keys[1]:
        vals = conn.get(key)
        vals = vals.decode()
        # print(type(ast.literal_eval(vals)))
        lis.append(ast.literal_eval(vals))
    return(lis)

def get_searched_data(keyword):
    if keyword == "":
        data = get_data()
        return data
    else:
        keyword += '*'
    keys = conn.keys(keyword)
    lis = []
    for key in keys:
        vals = conn.get(key)
        vals = vals.decode()
        # print(type(ast.literal_eval(vals)))
        lis.append(ast.literal_eval(vals))
    return(lis)

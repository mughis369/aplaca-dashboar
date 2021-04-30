import csv
import os
from app import utils
from datetime import datetime


FILE='market_data.csv'
HEADER=[
    'Event Name', 
    'Symbol', 
    'Volume', 
    'Accumulated Volume', 
    'Official Open Price', 
    'VWAP', 
    'Open Price', 
    'Close Price', 
    'High Price', 
    'Low Price', 
    'Average Price', 
    'Time Beginning', 
    'Time Ending', 
    'Stream Type'
]



def write_bar(res):

    data = res.get("data")
    stream_type = res.get("stream")

    perform_write_check()

    if stream_type not in ['authorization', 'listening']:
        msg = f"Recieved Data:\n {res}"

        write( 
            [
                data.get("ev", None),
                data.get("T",  None),
                data.get("v",  None),
                data.get("av", None),
                data.get("op", None),
                data.get("vw", None),
                data.get("o",  None),
                data.get("c",  None),
                data.get("h",  None),
                data.get("l",  None),
                data.get("a",  None),
                f'{datetime.fromtimestamp(data.get("e",  None)//1000)}',
                f'{datetime.fromtimestamp(data.get("s",  None)//1000)}',
                stream_type
            ]
        )

    else:
        msg = f"Recieved Other Message:\n {res}"
    
    print(msg)

def write(bar):
    try:
        with open(FILE, 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(bar)
            utils.set_last_update(f'{datetime.now()}'[:19])
    except Exception as ex:
        print(f"Error occured while writing to csv: {ex}")

def perform_write_check():
    if not os.path.isfile(FILE):
        with open(FILE, 'a') as csv_file:
            pass

def read(limit=None, sort=None):
    selected_records = []
    try:
        with open(FILE, 'r') as csv_file:
            records = list(csv.reader(csv_file, delimiter=','))

            print(sort, limit)

            if sort == 'latest':
                selected_records = records[::-1][:limit]
            elif sort == 'oldest':
                selected_records = records[:limit]
            else:
                raise ValueError("reverse expects a integer value of 0 or 1: (True, False)")
    except Exception as ex:
        print(f"Error occured while reading from csv: {ex}")
    finally:
        return HEADER, selected_records



# if __name__=="__main__":
#     import random
#     streams = "AM.SPY,AM.TSLA,AM.AAPL,AM.WORK,AM.MSFT,AM.GME,AM.LUV,AM.INTC,AM.AMC,AM.HOG".split(',')    

#     # populate csv with random data for testing

#     for i in range(1000):
#         stream = streams[random.randint(0, len(streams)-1)]
#         res =  {
#             'stream': f"{stream}-{i+1}", 
#             'data': {
#                 'ev': stream.split('.')[0], 
#                 'T': stream.split('.')[1], 
#                 'v': random.randint(0, 1000), 
#                 'av': random.randint(0, 1000), 
#                 'op': random.randint(0, 1000), 
#                 'vw': random.randint(0, 1000), 
#                 'o': random.randint(0, 1000), 
#                 'c': random.randint(0, 1000), 
#                 'h': random.randint(0, 1000), 
#                 'l': random.randint(0, 1000), 
#                 'a': random.randint(0, 1000), 
#                 's': 1347516459425, 
#                 'e': 1347516459425
#             }
#         }
#         write_bar(res)
        
#     # to view data

#     # prints rows from tail
#     for row in read(limit=5, reverse=True):
#         print(row)

#     # print rows from head 
#     for row in read(limit=5):
#         print(row)

#     # generate header
#     data = []
#     for item in HEADER:
#         words = item.split(' ')
#         initial = ''
#         for word in words:
#             initial += word[0]
#         data.append((initial, item))
#     print(data)

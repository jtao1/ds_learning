# from google.oauth2 import service_account
# from google.cloud import storage

# def read_file(stock):
#     bucket_name = 'streamlit-stocks-data'
#     credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
#     client = storage.Client(credentials=credentials)
#     bucket = client.bucket(bucket_name)
#     blob = bucket.get_blob(f'{stock}.csv')
#     df = []
#     content = ''
#     if storage.Blob(bucket=bucket, name=f'{stock}.csv').exists(client) and str(blob.updated)[:10] == str(dt.date.today()): 
#         #checks if the file stock exists and if its last updated and if it isn't we will upload a new version
#         content = bucket.blob(f'{stock}.csv').download_as_string().decode("utf-8")
#     else: 
#         data = yf.Ticker(stock)
#         data = data.history('3mo')
#         data.reset_index(inplace=True)
#         upload_blob(pd.DataFrame.to_string(data), f'{stock}.csv')
#         content = bucket.blob(f'{stock}.csv').download_as_string().decode("utf-8")
#     if len(content) == 84:
#          raise Exception()
#     else:
#         content = content.strip().split('\n') #if content array is 1, raise invalid stock error
#         for row in content[1:]:
#             row = row.split(' ')
#             row = row[1:]
#             while '' in row:
#                 row.remove('')
#             date = row[0]
#             row = [float(e) for e in row[1:]]
#             row.insert(0, date)
#             df.append(row)
#         df = pd.DataFrame(df, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
#         return df

# def upload_blob(contents, destination_name):
#     credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
#     client = storage.Client(credentials=credentials)
#     bucket = client.get_bucket('streamlit-stocks-data')
#     blob = bucket.blob(destination_name)
#     blob.upload_from_string(contents)
    
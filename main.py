from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib
import cryptocompare
from google.cloud import storage
import io
import ast
import pandas as pd

# Get the bucket that the file will be uploaded to.
storage_client = storage.Client()
bucket = storage_client.bucket('buick')

 # Create a new blob and upload the file's content.
my_file = bucket.blob('btc_data.csv')
my_file_w = bucket.blob('btc_data.csv')

def send_mail(df, compare_data):
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect('smtp.gmail.com', 587)
    
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("stjepan303@gmail.com", "aujjflscohncjvvn")
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"CUR: {curr_btc}, LAST:{compare_data.iloc[1, 2]}"
    msg['From'] = "stjepan303@gmail.com"
    msg['To'] = "sstjepan303@gmail.com"

    html = f"""\
    <html>
    <head></head>
    <body>
        {init_btc_data}
    </body>
    </html>
    """

    part2 = MIMEText(html, 'html')
    msg.attach(part2)
   
    server.sendmail(
        'stjepan303@gmail.com',
        'stjepan303@gmail.com',
        msg.as_string())
    
    server.quit()
            

btc_start = 964
btc_amnt = 0.02304

curr_btc = round(cryptocompare.get_price('BTC', currency='EUR')['BTC']['EUR']*btc_amnt)

change = f'{round((curr_btc-btc_start)/btc_start*100, 2)} %'

init_btc_data = {'gain':change, 'last':curr_btc, 'init':btc_start}

#pd.DataFrame([init_btc_data]).to_csv('gs://buick/btc_data.csv')

# Download the contents of the blob as a string and then parse it using json.loads() method
compare_data = pd.read_csv('gs://buick/btc_data.csv')

diff = curr_btc/int(compare_data.iloc[1, 2])

def crypto(init_btc_data):

    # my_file_w.upload_from_string(data=jsonify(init_btc_data),content_type='application/json')
    df = pd.DataFrame(list(init_btc_data.items()))
    df.to_csv('gs://buick/btc_data.csv')

    if diff > 1.001:
        send_mail(init_btc_data, compare_data)

    elif diff < 0.999:
        send_mail(init_btc_data, compare_data)


crypto(init_btc_data)






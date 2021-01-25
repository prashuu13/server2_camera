import google.cloud.storage as storage
import os
from imutils import paths
from datetime import datetime as dt
import psycopg2
import pytz
tz = pytz.timezone("Asia/Calcutta")
conn = psycopg2.connect(host="datavivservers.in", port = 5436, database="camerax", user="Dataviv", password="DatavivPostgreSQLSecurePassword!")
cur = conn.cursor()
# conn = psycopg2.connect(host="35.232.103.138", port = 5432, database="camerax", user="datavivai2085", password="secure@dataviv123")
# cur = conn.cursor()

def meta_data_store(img_url, timestamp, classtype,store_id,ownerid):
# cur.execute("""SELECT * FROM camera_modelanalysis""")
# img_url = "https://storage.googleapis.com/camerax-bucket/images/0/201001/14/Customer/fed2.jpg"
# timestamp ="2020-09-06T07:59:43.975597Z"
# classtype ="E"
# store_id = 9
    # try:
    #sql = "INSERT into camera_modelanalysis2(img_url,timestamp,classtype,store_id,owner_id,flag) values('%s', '%s', '%s',%d, %r)" % (img_url, timestamp, classtype, int(store_id),int(ownerid),False)
    sql = "INSERT into camera_socialdistancing2(img_url,timestamp,flag,owner_id) values('%s','%s',%r,%d)"%(img_url,timestamp,False,int(ownerid))
    cur.execute(sql)
    conn.commit()

    # query_results = cur.fetchall()
    # print(query_results)

    # cur.close()
    # conn.close()
    return 0
    # except:
    #     return 1

new_key = 'melodic-eye-296511-ce1ca7a5bc8e.json'
def store_image_bucket(storeid,clas,imgname,ownerid):
 
    storage_client = storage.Client.from_service_account_json(os.path.abspath(new_key))
    bucket = storage_client.get_bucket("camerax")
    _,FILENAME = os.path.split(imgname)
    datepath = dt.now(tz).strftime('%y%m%d')
    hour = dt.now(tz).hour
    timestamp = dt.now(tz)
    FILENAME = f"images/{storeid}/{datepath}/{hour}/{clas}/{FILENAME}"
    blob = bucket.blob(FILENAME)
    blob.upload_from_filename(imgname)
    blob.make_public()
    url = blob.public_url
    # meta = {'url':url, 'storeid':storeid, 'class':clas, 'timestamp': timestamp}
    # img_url, timestamp, classtype,store_id
    ret = meta_data_store(url,timestamp,clas,storeid,ownerid)
    print(url,ret)
    return url
def social_store_image_bucket(storeid,clas,imgname,ownerid):
 
    storage_client = storage.Client.from_service_account_json(os.path.abspath(new_key))
    bucket = storage_client.get_bucket("camerax")
    _,FILENAME = os.path.split(imgname)
    datepath = dt.now(tz).strftime('%y%m%d')
    hour = dt.now(tz).hour
    timestamp = dt.now(tz)
    FILENAME = f"images/sd/{storeid}/{datepath}/{hour}/{clas}/{FILENAME}"
    blob = bucket.blob(FILENAME)
    blob.upload_from_filename(imgname)
    blob.make_public()
    url = blob.public_url
    # meta = {'url':url, 'storeid':storeid, 'class':clas, 'timestamp': timestamp}
    # img_url, timestamp, classtype,store_id
    ret = meta_data_store(url,timestamp,clas,storeid,ownerid)
    print(url,ret)
    print(url)
    return url
def insert_analysis1(avg_male_count, avg_female_count, age_child, age_teenge, age_adult, age_old, total_in,total_out,customer_walkin, store_id):
    try:
        # print(avg_male_count, avg_female_count, age_child, age_teenge, age_adult, age_old, total_in,total_out,customer_walkin, store_id)
        timestamp = dt.now(tz)
        sql = "INSERT into camera_analysis1(avg_male_count, avg_female_count, age_child, age_teenge, age_adult, age_old, total_in,total_out,customer_walkin, timestamp, store_id) values( %d, %d, %d, %d, %d, %d, %d, %d, %d,'%s', %d)" % (int(avg_male_count), int(avg_female_count), int(age_child), int(age_teenge), int(age_adult), int(age_old), int(total_in),int(total_out),int(customer_walkin), timestamp, int(store_id))
        cur.execute(sql)
        conn.commit()
    # cur.close()
    # conn.close()
        return 1
    except:
        # cur.execute("ROLLBACK")
        # pass
        # conn.commit()
        # cur.execute(sql)s
        # conn.commit()
        return -1

def insert_analysis2(avg_purchased_visit,avg_linelength,timestamp,store_id):
    try:
        sql = "INSERT into camera_analysis2(avg_purchased_visit,avg_linelength,timestamp,store_id) values(%d, %d,'%s',%d )" % (int(avg_purchased_visit), int(avg_linelength), timestamp, int(store_id))
        cur.execute(sql)
        conn.commit()

        # cur.close()
        # conn.close()
        return 1
    except:
        return -1
# img = 'images/278775078_11142020231136403467.jpg'
# url = store_image_bucket(str(0),"O",img)
# print(url)
# path = 'data_dumps/employ_data'
# imagePaths = sorted(list(paths.list_images(path)))

# for imgpath in imagePaths:
#     print(imgpath)
#     ret = store_image_bucket(str(9),'E',imgpath)
#     print(ret)
# print(insert_analysis1(avg_male_count=10, avg_female_count=8, age_child=1, age_teenge=2, age_adult=16, age_old=0, total_in=14,total_out=11,customer_walkin=8, store_id=9))

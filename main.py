from fastapi import FastAPI
from enum import Enum
import json
from pydantic import BaseModel
from typing import Optional
import datetime
import cx_Oracle
import mysql.connector
import uvicorn
import os,time
import socket
# from sqlalchemy import create_engine,Table,Column,Integer,String, MetaData
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
import cx_Oracle


app = FastAPI()

# time.tzset()
dt = datetime.datetime.now()
dtyear = dt.year
dtmonth = dt.month
dtday = dt.day
dthour = dt.hour
dtmnt = dt.minute
dtsec = dt.second
datefix = dtday + dtmonth + dtyear
# os.environ['TZ'] = 'Asia/Jakarta'
# dt.tzset()


jadwalHadirAbsen = dt.date()

os.environ['TZ'] = 'Asia/Jakarta'
jamhadir = time.strftime('%H:%M')
print(jamhadir)


# dateTimeNow = datefix

# jamhadir = str(dthour) + ":" + str(dtsec)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# engine = create_engine("mysql///?User=root&Password=&Database=project_absensi&Server=localhost&Port=3306",echo = True)
host = '10.1.0.10'
port = 1521
sid = 'rsmhdb'
user = 'sdm'
passw = 'peg_2015'
sid = cx_Oracle.makedsn(host,port,sid = sid)
cstr = 'oracle://{user}:{passw}@{sid}'.format(
    user = user,
    passw = passw,
    sid = sid
)
engine = create_engine(cstr,echo = True)
# engine.cursor()
# engine.connect()




class Absen(BaseModel):
    pin: str
    lat: str
    ip_address : str
    long: str
    verif: int
    is_dm: int
    image : str

    class Config:
        schema_extra = {
            "example": {
                "pin": 12345,
                "lat": "-6.917464",
                "long": "107.619125",
                "ip_address": "127.0.0.1",
                "verif" : 1,
                "is_dm" : 0,
                "image" : "98789127hgfksad128"
            }
        }


class Peserta(BaseModel):
    nama: str
    nip: int
    # namaUpdate : Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "nama": "Nama Peserta",
                "nip": 12345,
            }
        }


class UpdatePeserta(BaseModel):
    nama: str
    nip: int

    class Config:
        schema_extra = {
            "example": {
                "nama": "Kucing Garong",
                "nip": 12345,
            }
        }


class DeletePeserta(BaseModel):
    nip: int

    class Config:
        schema_extra = {
            "example": {
                "nip": 12345,
            }
        }


@app.get('/')
def index():
    # result = engine.execute('select * FROM DATA_ABSEN')
    # print(result.)
    # print(result[0])
    # print(result)
    # for row in result:
    #     print(row)
    return {"hello world"}


@app.post('/absen/')
def submitAbsen(absen: Absen):
    # waktuhadir = absen.waktuKehadiran
    pin = absen.pin
    lat = absen.lat
    ip_address = absen.ip_address
    long = absen.long
    is_dm = absen.is_dm
    verif = absen.verif
    location = lat + " - " + long
    imagebase64 = absen.image
    print(imagebase64)
    # sql = ("insert into DEMO_ABSEN(PIN, IP_ADDRESS, TGL, JAM,VERIF,LOCATION,IS_DM,IMAGE_BASE64) values(:1,:2,DATE :3,:4,:5,:6,:7,:8)")
    row_data = [(pin,ip_address,jadwalHadirAbsen,jamhadir,verif,location,is_dm,imagebase64)]
    # engine.execute("INSERT INTO DEMO_ABSEN(PIN, IP_ADDRESS, TGL, JAM,VERIF,LOCATION,IS_DM,IMAGE_BASE64) values(:1,:2,:3,:4,:5,:6,:7,:8)",row_data)
    engine.execute("INSERT INTO DEMO_ABSEN(PIN, IP_ADDRESS,TGL, JAM,VERIF,LOCATION,IS_DM,IMAGE_BASE64) values(:1,:2,:3,:4,:5,:6,:7,:8)",row_data)
    # engine.execute(sql,{'pin' : pin,'ip_address' : 'localhost','tgl':datefix,'jam':jamhadir,'verif':verif,'location':location,'is_dm':is_dm,'image_base64':imagebase64})
    # engine.close()
    # engine.commit()
    # engine.close()
    # engine.execute("INSERT INTO `DEMO_ABSEN`(`PIN`, `IP_ADDRESS`, `TGL`, `JAM`,`VERIF`,`LOCATION`,`IS_DM`,`IMAGE_BASE64`) VALUES ({PIN}, {IP_ADDRESS},DATE {TGL},{JAM},{VERIF},{LOCATION},{IS_DM},{IMAGE_BASE64})").format(
    #     PIN = pin,
    #     IP_ADDRESS = 'localhost',
    #     TGL = datefix,
    #     JAM = jamhadir,
    #     VERIF = verif,
    #     LOCATION = 
    #     IS_DM = is_dm,
    #     IMAGE_BASE64 = imagebase64

    # )


    pesertanya = absen.dict()
    
    sukses = {'response': [{'code': '200'}, {'message': 'success'}]}
    resp = dict(sukses)
    resp.update(pesertanya)
    return resp


# @app.post('/insertpeserta/')
# def insertPeserta(peserta: Peserta):
#     nip = peserta.nip
#     nama = peserta.nama
#     cursor = mydb.cursor()
#     cursor.execute(
#         "INSERT INTO `user`(`nip`, `nama`) VALUES (%d, '%s')" % (nip, nama))
#     mydb.commit()
#     mydb.close()
#     data = peserta.dict()
#     sukses = {'response': [{'code': '200'}, {'message': 'success'}]}
#     resp = dict(sukses)
#     resp.update(data)
#     return resp


# @app.post('/updatepeserta/')
# def updatePeserta(peserta: UpdatePeserta):
#     nip = peserta.nip
#     namaGanti = peserta.nama
#     cursor = mydb.cursor()
#     cursor.execute("UPDATE `user` SET `nama`='%s' WHERE `nip`= %d" %
#                    (namaGanti, nip))
#     mydb.commit()
#     mydb.close()
#     data = peserta.dict()
#     sukses = {'response': [{'code': '200'}, {'message': 'success'}]}
#     resp = dict(sukses)
#     resp.update(data)
#     return resp


# @app.post('/deletepeserta/')
# def deletePeserta(peserta: DeletePeserta):
#     nip = peserta.nip
#     # nama = peserta.nama
#     cursor = mydb.cursor()
#     cursor.execute("DELETE FROM `user` WHERE `nip` = %d" % (nip))
#     mydb.commit()
#     mydb.close()
#     data = peserta.dict()
#     sukses = {'response': [{'code': '200'}, {'message': 'success'}]}
#     resp = dict(sukses)
#     resp.update(data)
#     return resp


if __name__ == "__main__":
    uvicorn.run(app, host=IPAddr, port=8000)

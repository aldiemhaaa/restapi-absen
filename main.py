from fastapi import FastAPI
from enum import Enum
import json
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import cx_Oracle
import mysql.connector
import uvicorn
import socket

app = FastAPI()

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="project_absensi")

dt = datetime.now()
dtyear = dt.year
dtmonth = dt.month
dtday = dt.day
dthour = dt.hour
dtmnt = dt.minute
dtsec = dt.second
datefix = str(dtyear) + "-" + str(dtmonth) + "-" + str(dtday) + " " +  str(dthour) + ":" +  str(dtmnt) + ":" +  str(dtsec)
dateTimeNow = datefix
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    


class Absen(BaseModel):
    nip: int
    namaPeserta: Optional[str]= None
    lat : str
    long : str
    waktuKehadiran : Optional[str] = dateTimeNow
    
    class Config:
        schema_extra = {
            "example": {
                "nip": 12345,
                "namaPeserta": "Nama Peserta",
                "lat": "-6.917464",
                "long": "107.619125",
            }
        }

class Peserta(BaseModel):
    nama : str
    nip : int
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
    nip : int
    class Config:
        schema_extra = {
            "example": {
                "nama": "Kucing Garong",
                "nip": 12345,
            }
        }

class DeletePeserta(BaseModel):
    nip : int

    class Config:
        schema_extra = {
            "example": {
                "nip": 12345,
            }
        }


@app.post('/absen/')
def submitAbsen(absen : Absen):
    waktuhadir = absen.waktuKehadiran
    nip = absen.nip
    lat = absen.lat
    long = absen.long
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO `absensi`(`nip`, `waktu_absen`, `lati_maps`, `long_maps`) VALUES (%d, '%s','%s','%s')" % (nip, waktuhadir,lat , long))
    mydb.commit()
    mydb.close()
    pesertanya = absen.dict()
    # print(pesertanya)
    sukses = {'response': [{'code':'200'},{'message': 'success'}]}
    resp = dict(sukses)
    resp.update(pesertanya)
    return resp


@app.post('/insertpeserta/')
def insertPeserta(peserta : Peserta):
    nip = peserta.nip
    nama = peserta.nama
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO `user`(`nip`, `nama`) VALUES (%d, '%s')" % (nip,nama))
    mydb.commit()
    mydb.close()
    data = peserta.dict()
    sukses = {'response': [{'code':'200'},{'message': 'success'}]}
    resp = dict(sukses)
    resp.update(data)
    return resp

@app.post('/updatepeserta/')
def updatePeserta(peserta: UpdatePeserta):
    nip = peserta.nip
    namaGanti = peserta.nama
    cursor = mydb.cursor()
    cursor.execute("UPDATE `user` SET `nama`='%s' WHERE `nip`= %d" % (namaGanti,nip))
    mydb.commit()
    mydb.close()
    data = peserta.dict()
    sukses = {'response': [{'code':'200'},{'message': 'success'}]}
    resp = dict(sukses)
    resp.update(data)
    return resp

@app.post('/deletepeserta/')
def deletePeserta(peserta:DeletePeserta):
    nip = peserta.nip
    # nama = peserta.nama
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM `user` WHERE `nip` = %d" % (nip))
    mydb.commit()
    mydb.close()
    data = peserta.dict()
    sukses = {'response': [{'code':'200'},{'message': 'success'}]}
    resp = dict(sukses)
    resp.update(data)
    return resp
   
if __name__ == "__main__":
    uvicorn.run(app,host=IPAddr,port =8000)
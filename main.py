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

class Peserta(BaseModel):
    nama : str
    nip : int
    # namaUpdate : Optional[str] = None

class UpdatePeserta(BaseModel):
    nama: str
    nip : int

class DeletePeserta(BaseModel):
    nip : int


@app.get("/")
async def index():
    return {"message":"Hello World"}


@app.post('/absen/')
def submitAbsen(absen : Absen):
    try:
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
    except:
        mydb.rollback()
        raise
        return "error"


@app.post('/insertpeserta/')
def insertPeserta(peserta : Peserta):
    try:
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
    except:
        mydb.rollback()
        raise
    

@app.post('/updatepeserta/')
def updatePeserta(peserta: UpdatePeserta):
    try:
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
    except:
        mydb.rollback()
        raise

@app.post('/deletepeserta/')
def deletePeserta(peserta:DeletePeserta):
    try:
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
    except:
        mydb.rollback()
        raise

if __name__ == "__main__":
    uvicorn.run(app,host=IPAddr,port =8000)
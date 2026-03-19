# service-locker/main.py

from fastapi import FastAPI, HTTPException
import mysql.connector

app = FastAPI()

# Slave DB 연결 정보 (.9 서버)
db_config = {
    'host': '172.16.0.9',
    'user': 'root',
    'password': '1234',
    'database': 'locker_system'
}

@app.get("/api/lockers/{station}")
async def get_lockers(station: str):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        # HTML 반영을 위해 locker_num을 id로 반환
        query = "SELECT locker_num as id, status FROM lockers WHERE station_name = %s ORDER BY locker_num"
        cursor.execute(query, (station,))
        lockers = cursor.fetchall()
        conn.close()
        return lockers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

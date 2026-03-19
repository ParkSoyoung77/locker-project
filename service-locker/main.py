# service-locker/main.py
from fastapi import FastAPI, HTTPException
import mysql.connector
import os  # 환경변수를 읽기 위해 추가

app = FastAPI()

# 환경변수에서 정보를 가져오고, 없으면 기본값(Default)을 사용함
db_config = {
    'host': os.getenv('DB_HOST', 'mariadb-master-svc'),
    'user': os.getenv('DB_USER', 'sy_user'),
    'password': os.getenv('DB_PASS', '1234'),
    'database': os.getenv('DB_NAME', 'locker_system')
}

@app.get("/api/lockers/{station}")
async def get_lockers(station: str):
    try:
        # DB 연결 시도
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # 쿼리 실행
        query = "SELECT locker_num as id, status FROM lockers WHERE station_name = %s ORDER BY locker_num"
        cursor.execute(query, (station,))
        lockers = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return lockers
    except Exception as e:
        # 에러 발생 시 상세 메시지 반환
        raise HTTPException(status_code=500, detail=str(e))

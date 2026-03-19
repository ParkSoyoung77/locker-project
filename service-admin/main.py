from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel

app = FastAPI()

# Master DB 연결 정보 (.8 서버)
db_config = {
    'host': '172.16.0.8',
    'user': 'root',
    'password': '1234',
    'database': 'locker_system'
}

# 1. 전체 사물함 상세 현황 조회 (비밀번호, 전화번호 포함)
@app.get("/api/admin/lockers")
async def get_admin_lockers():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        # 관리자용이므로 모든 컬럼을 조회합니다.
        query = "SELECT * FROM lockers ORDER BY station_name, locker_num"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. 특정 사물함 강제 초기화 (비우기)
@app.post("/api/admin/reset/{locker_id}")
async def reset_locker(locker_id: int):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # 해당 사물함을 초기 상태(0000, NULL, available)로 되돌림
        query = """
            UPDATE lockers 
            SET password = '0000', phone = NULL, status = 'available' 
            WHERE id = %s
        """
        cursor.execute(query, (locker_id,))
        conn.commit()
        conn.close()
        return {"message": f"Locker {locker_id} has been reset."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

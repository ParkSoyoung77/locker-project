from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

class Reservation(BaseModel):
    station: str
    locker_id: int
    password: str
    phone: str

# Master DB 연결 정보 (.8 서버)
db_config = {
    'host': '172.16.0.8',
    'user': 'root',
    'password': '1234',
    'database': 'locker_system'
}

@app.post("/api/reserve")
async def reserve_locker(res: Reservation):
    # [비밀번호 정책 반영] 0000 차단 로직
    if res.password == "0000":
        raise HTTPException(status_code=400, detail="0000은 초기 비밀번호이므로 사용할 수 없습니다.")

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # 1. 사물함 상태 업데이트
        query = """
            UPDATE lockers 
            SET password = %s, phone = %s, status = 'occupied' 
            WHERE station_name = %s AND locker_num = %s AND status = 'available'
        """
        cursor.execute(query, (res.password, res.phone, res.station, res.locker_id))
        
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=400, detail="이미 예약되었거나 존재하지 않는 사물함입니다.")
            
        conn.commit()
        conn.close()
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

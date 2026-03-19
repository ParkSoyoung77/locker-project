from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import os  # 환경변수를 읽기 위해 추가

app = FastAPI()

class Reservation(BaseModel):
    station: str
    locker_id: int
    password: str
    phone: str

# 쿠버네티스 환경변수에서 정보를 가져옴 (기본값 설정 포함)
db_config = {
    'host': os.getenv('DB_HOST', 'mariadb-master-svc'),
    'user': os.getenv('DB_USER', 'sy_user'),
    'password': os.getenv('DB_PASS', '1234'),
    'database': os.getenv('DB_NAME', 'locker_system')
}

@app.post("/api/reserve")
async def reserve_locker(res: Reservation):
    # [비밀번호 정책 반영] 0000 차단 로직
    if res.password == "0000":
        raise HTTPException(status_code=400, detail="0000은 초기 비밀번호이므로 사용할 수 없습니다.")

    try:
        # DB 연결 시도
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 1. 사물함 상태 업데이트
        # available 상태인 것만 occupied로 변경하는 로직
        query = """
            UPDATE lockers 
            SET password = %s, phone = %s, status = 'occupied' 
            WHERE station_name = %s AND locker_num = %s AND status = 'available'
        """
        cursor.execute(query, (res.password, res.phone, res.station, res.locker_id))

        # 업데이트된 행이 0개라면 (이미 예약됐거나 정보가 틀린 경우)
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="이미 예약되었거나 존재하지 않는 사물함입니다.")

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "success"}
    except Exception as e:
        # 에러 발생 시 상세 메시지 반환
        raise HTTPException(status_code=500, detail=str(e))

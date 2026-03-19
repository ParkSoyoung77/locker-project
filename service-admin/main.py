from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
import os  # 환경변수를 읽기 위해 추가

app = FastAPI()

# 쿠버네티스 환경변수에서 DB 접속 정보를 동적으로 가져옵니다.
db_config = {
    'host': os.getenv('DB_HOST', 'mariadb-master-svc'),
    'user': os.getenv('DB_USER', 'sy_user'),
    'password': os.getenv('DB_PASS', '1234'),
    'database': os.getenv('DB_NAME', 'locker_system')
}

# 1. 전체 사물함 상세 현황 조회 (비밀번호, 전화번호 포함)
@app.get("/api/admin/lockers")
async def get_admin_lockers():
    try:
        # DB 연결 시도
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # 관리자용이므로 모든 컬럼을 조회합니다.
        query = "SELECT * FROM lockers ORDER BY station_name, locker_num"
        cursor.execute(query)
        result = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        # 에러 발생 시 상세 메시지 반환 (디버깅용)
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
        cursor.close()
        conn.close()
        return {"message": f"Locker {locker_id} has been reset."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

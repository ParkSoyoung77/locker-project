# 1. 베이스 이미지 선택 (경량화된 slim 버전 권장)
FROM python:3.9-slim
# 2. 작업 디렉토리 생성 및 이동
WORKDIR /app
# 3. 환경 변수 설정 (Python이 .pyc 파일을 생성하지 않고, 로
그를 즉시 출력하도록 설정)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# 4. 의존성 파일 먼저 복사 (캐시 최적화)
COPY requirements.txt .
# 5. 주요 라이브러리 설치
# --no-cache-dir 옵션으로 이미지 용량을 줄입니다.
RUN pip install --no-cache-dir -r requirements.txt
# 6. 소스 코드 전체 복사
COPY . .
# 7. 포트 노출 (문서화용)
EXPOSE 8001
# 8. 앱 실행 명령 (ENTRYPOINT와 CMD 조합으로 유연성 확보)
# 0.0.0.0으로 설정해야 컨테이너 외부에서 접속 가능합니다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

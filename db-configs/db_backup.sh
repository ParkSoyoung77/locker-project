#!/bin/bash

# [추가] 크론탭 실행을 위한 환경 변수 설정
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 1. 설정
BACKUP_DIR="/mnt/db_backup"
DATE=$(date +%Y%m%d_%H%M%S)
FILE_NAME="db_full_$DATE.sql"

# [추가] 마운트 체크: 마운트가 안 되어 있으면 로컬 디스크를 보호하기 위해 종료
if ! mountpoint -q "$BACKUP_DIR"; then
    echo "Error: $BACKUP_DIR is not mounted! Backup aborted to save local disk space."
    exit 1
fi

# [추가] 권한 설정: 그룹에도 쓰기 권한(664)을 주기 위해 umask 설정
umask 002

# 2. 백업 실행 (비밀번호 1234)
# > 대신 -r (result) 옵션을 쓰거나 파이프를 쓰는 방식도 있지만, 현재 방식도 작동합니다.
mysqldump -u root -p1234 --all-databases > "$BACKUP_DIR/$FILE_NAME"

# 3. 소유권 변경 (UID 1001:share_user)
# sudo를 쓰려면 crontab 실행 시 password 없는 sudo 권한이 필요할 수 있습니다.
sudo chown 1001:1001 "$BACKUP_DIR/$FILE_NAME"

# 4. 오래된 파일 삭제 (7일 경과)
find "$BACKUP_DIR" -type f -name "*.sql" -mtime +7 -delete

echo "Backup completed: $FILE_NAME"

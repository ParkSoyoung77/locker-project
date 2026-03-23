# 가이드라인

1. vm웨어 다 켜기

2. 설정
k8s-m: kubectl port-forward svc/grafana 3000:80 --address 0.0.0.0
db-m: sudo mysql -u root -p => use locker_system => select * from lockers;
db-s: cd /mnt/db_backup

3. 그라파나
Loki: namesapce를 locker-view-ns로 설정

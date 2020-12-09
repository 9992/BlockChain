### 구축환경

| SW 및 모듈 정보 | 버전 |
| --- | ---|
| Chrome | v74.0 |
| VS Code | v1.33.1|
| HeidiSQL | v10.1|
| Postman | v7.0.9|
| Node.JS | v12.1.0|
| npm | v6.9.0|
| Python | v3.7.3|
| Flask | v0.12.2|
| Create-React-App | v3.0.1 |
| nodemon | v1.19.0 |
| pymysql | v0.9.3 |

| AWS | 정보 |
| --- | ---|
| MySQL | v5.6.40 |
| vCPU | 1thread |
| RAM | 1GB |
| SSD | 20GB |


### 실행 순서

1. 블록체인 서버 start
2. 데이터 입력 
3. 해시함수별(3개의 난이도 쉬움/보통/어려움) 블록 생성 속도 측정

### 테스트 케이스

80자, 5000자, 10000자 데이터 100개로 간의 테스트 예정
테스트 케이스 실행 후 마지막 검증으로 각 노드의 데이터에 블록이 공유가 되었음을 확인하는 POST 명령을 실시

### 시스템 프로세스 

<img src="https://i.ibb.co/rb3kKsV/image.png" alt="image" border="0">

# todos

```
fastapi simple todos app
```

## python 가상환경 만들기

```
python -m venv fa_venv
```

## 가상환경 활성화

```
[windows]
fa_venv/scripts/activate

[mac/linux]
source fa_venv/bin/activate
```

## 설치 라이브러리

### 기본

```
pip install fastapi
pip install "uvicorn[standard]"
pip install jinja2 python-multipart
```

### DB ORM 및 mysql 연동

```
pip install sqlalchemy
pip install pymysql
```

### db_env 모듈 예시

- 파일명 : db_env.py

```
host = "localhost"
user = "test"
password = "test"
db_name = "testdb"
```

## 서버 실행방법

```
python app_start.py
```

## todos 클라이언트 테서트

```
[앱 실행]
http://localhost:8000

[스웨거]
http://localhost:8000/docs
```

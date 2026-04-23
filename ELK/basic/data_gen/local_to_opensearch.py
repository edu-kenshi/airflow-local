'''
- 로그(데이터) 발생 -> opensearch -> 직접 전송
- pip install -q opensearch-py
- 구동
    python ./ELK/basic/data_gen/local_to_opensearch.py
'''
# 1. 모듈 가져오기
from opensearchpy import OpenSearch
from datetime import datetime
import random
import time

# 2. 환경변수
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('OPENSEARCH_HOST')
AUTH = (os.getenv('AUTH_NAME'), os.getenv('AUTH_PW'))
print(HOST, AUTH)

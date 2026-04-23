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

# 2. 환경변수 설정
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('OPENSEARCH_HOST')
AUTH = (os.getenv('AUTH_NAME'), os.getenv('AUTH_PW'))
print(HOST, AUTH)

# 3. AWS Opensearch 서비스 클라이언트 연결
client = OpenSearch(
    hosts         = [{"host": HOST, "port": 443}], # https -> 443
    http_auth     = AUTH,
    http_compress = True,
    use_ssl       = True,
    verify_certs  = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

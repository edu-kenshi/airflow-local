'''
- ma 에서 gold 단계 처리
- 최종 형태의 데이터셋 구성, View 형식으로 구성
'''
# 1. 모듈 가져오기
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.athena import AthenaOperator

# 2. 환경변수
DATABASE_SILVER = 'de_ai_30_ma_silver_db'
DATABASE_GOLD   = 'de_ai_30_ma_gold_db'
# 쿼리 히스토리등 저장용 -> 메타
ATHENA_RESULTS  = 's3://de-ai-30-827913617635-ap-northeast-2-an/athena-results/'
# 임시로 증분용 테이블이 아닌 ctas용 테이블 참조 조정
SILVER_TBL_NAME = 'sales_silver_tbl' #'sales_silver_increment_tbl'
GOLD_VIEW_NAME  = 'daily_sales_summary_gold_view'

# 3. DAG 정의
with DAG(
    dag_id      = "12_medallion_silver_to_gold_view", 
    description = "gold 단계",
    default_args= {
        'owner'             : 'de_2team_manager',        
        'retries'           : 1,
        'retry_delay'       : timedelta(minutes=1)
    },
    # 모든 매장은 21시에 마감한다 (설정)
    schedule_interval = '@daily', # 00시00분00초에 스케줄 작동
    start_date  = datetime(2026,2,25),     
    catchup     = False,
    tags        = ['aws', 'medallion', 'gold', 'athena', 'view'],
) as dag:
    # 작동하면 최신 정보까지 모두 수집함 -> 가상테이블
    create_gold_view = AthenaOperator(
        task_id='create_or_replace_gold_view',
        query="""
            CREATE EXTERNAL TABLE IF NOT EXISTS {{ params.database_silver }}.{{ params.tbl_nm }} (
                event_id string,
                event_timestamp timestamp,
                user_id string,
                item_id string,
                price int,
                qty int,
                total_price int,
                store_id string,
                source_ip string,
                user_agent string
            )
            PARTITIONED BY (dt string, hr string)
            STORED AS PARQUET
            LOCATION '{{ params.silver_path }}'
            TBLPROPERTIES ('parquet.compress'='SNAPPY');
        """,
        params={
            'database_gold'  : DATABASE_GOLD,
            'database_silver': DATABASE_SILVER,            
            'view_nm'        : GOLD_VIEW_NAME,
            'table_nm'       : SILVER_TBL_NAME,
        },
        database=DATABASE_GOLD,
        output_location=ATHENA_RESULTS
    )

    
    create_gold_view

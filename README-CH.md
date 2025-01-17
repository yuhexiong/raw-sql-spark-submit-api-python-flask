# Raw SQL Spark Submit API

提供 API 到 Hadoop Resource Manager 機器中提交 Raw SQL Data Pipeline 的後端服務。


## Overview

- 語言: Python v3.12
- 網頁框架: Flask v2.2.5

## Introduction

### API Implementation
- 讀取 Request Body 的參數並進行驗證
- 連線至 Resource Manager 機器中在 Spark Data Pipeline 的資夾內依照參數 filename 建立 Pipeline Yaml
- 在當前目錄提交 Data Pipeline Python 檔案與 Yaml 到 Spark 立即執行


## Step

1. 自行架設 Hadoop Yarn 以及 Spark
   
2. 將 Raw SQL Data Pipeline 的 Python 檔案以及所需 Jar 檔放置於機器當中  
參考 [Raw SQL Data Pipeline Spark](https://github.com/yuhexiong/raw-sql-data-pipeline-spark-python)  

3. 填寫環境變數  
    複製 `.env.example` 成 `.env` 並修改連線資訊  
    ```
    HOSTNAME=RESOURCE_MANAGER_HOST
    USERNAME=HADOOP_USERNAME
    PASSWORD=HADOOP_PASSWORD
    SPARK_HOME=SPARK_HOME
    SPARK_PIPELINE_DIR=SPARK_PIPELINE_DIR
    JARS=JARS
    PYTHON_FILE=mysql_raw_query.py
    ```

4. 啟動後端服務  
    ```bash
    python main.py
    ```
    後端服務運行於 `localhost:5000`  

5. 使用 API 提交 Data Pipeline  
    `POST /api/query`
    ```json
    {
        "filename": "example",
        "source": {
            "host": "localhost",
            "port": 9030,
            "database": "db",
            "user": "user",
            "password": "pass"
        },
        "sink": {
            "host": "localhost",
            "port": 9030,
            "database": "db",
            "user": "user",
            "password": "pass",
            "table": "table"
        },
        "query": "SELECT * FROM table"
    }
    ```
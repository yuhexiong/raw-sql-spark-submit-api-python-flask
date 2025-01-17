# Raw SQL Spark Submit API

Provides an API to submit Raw SQL Data Pipeline to the Hadoop Resource Manager backend service.

## Overview

- Language: Python v3.12
- Web Framework: Flask v2.2.5

## Introduction

### API Implementation
- Reads and validates the parameters in the Request Body
- Connects to the Resource Manager machine and creates the Pipeline YAML in the Spark Data Pipeline directory based on the `filename` parameter
- Submits the Data Pipeline Python file and YAML to Spark for immediate execution in the current directory

## Step

1. Set up Hadoop Yarn and Spark manually

2. Place the Raw SQL Data Pipeline Python file and required JAR files on the machine  
   Refer to [Raw SQL Data Pipeline Spark](https://github.com/yuhexiong/raw-sql-data-pipeline-spark-python)

3. Fill in environment variables  
   Copy `.env.example` to `.env` and modify the connection information  
   ```
   HOSTNAME=RESOURCE_MANAGER_HOST
   USERNAME=HADOOP_USERNAME
   PASSWORD=HADOOP_PASSWORD
   SPARK_HOME=SPARK_HOME
   SPARK_PIPELINE_DIR=SPARK_PIPELINE_DIR
   JARS=JARS
   PYTHON_FILE=mysql_raw_query.py
   ```

4. Start the backend service  
   ```bash
   python main.py
   ```  
   The backend service will run at `localhost:5000`

5. Use the API to submit the Data Pipeline  
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
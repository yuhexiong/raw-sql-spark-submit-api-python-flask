import os
from datetime import datetime

import paramiko
import yaml
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__)


def check_parameters(parameters):
    def recursive_check(obj, parent_key=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                recursive_check(
                    value, f"{parent_key}.{key}" if parent_key else key)
        else:
            if obj is None:
                raise ValueError(f"should provide parameter {parent_key}")

    try:
        recursive_check(parameters)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@app.route('/api/query', methods=['POST'])
def save_query():
    data = request.get_json()

    filename = data.get('filename')

    source_data = {
        'host': data.get('source', {}).get('host'),
        'port': data.get('source', {}).get('port'),
        'database': data.get('source', {}).get('database'),
        'user': data.get('source', {}).get('user'),
        'password': data.get('source', {}).get('password')
    }

    sink_data = {
        'host': data.get('sink', {}).get('host'),
        'port': data.get('sink', {}).get('port'),
        'database': data.get('sink', {}).get('database'),
        'user': data.get('sink', {}).get('user'),
        'password': data.get('sink', {}).get('password'),
        'table': data.get('sink', {}).get('table')
    }

    query_data = data.get('query')

    check_parameters({
        'source': source_data,
        'sink': sink_data,
        'query': query_data
    })

    config_data = {
        'source': source_data,
        'query': query_data,
        'sink': sink_data
    }

    full_filename = f"{filename}.yaml"
    with open(full_filename, 'w') as f:
        yaml.dump(config_data, f)

    stderr = execute_spark_job(full_filename)

    return jsonify({'spark_stderr': stderr})


def execute_spark_job(full_filename):
    hostname = os.getenv("HOSTNAME")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    spark_home = os.getenv("SPARK_HOME")
    spark_pipeline_dir = os.getenv("SPARK_PIPELINE_DIR")
    jars = os.getenv("JARS")

    python_file = os.getenv("PYTHON_FILE")
    if not python_file.endswith(".py"):
        python_file += ".py"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)

        print(f"[{current_time()}] Uploading {full_filename}...")
        sftp = client.open_sftp()
        sftp.put(f"{full_filename}", f"{spark_pipeline_dir}/{full_filename}")
        sftp.close()

        print(f"[{current_time()}] Spark Submitting...")
        command = f"cd {spark_pipeline_dir} && \
            {spark_home}/spark-submit \
            --master yarn \
            --deploy-mode cluster \
            --conf spark.driver.host={hostname} \
            --conf spark.executor.instances=1 \
            --conf spark.yarn.submit.waitAppCompletion=false \
            --jars {jars} \
            --py-files {python_file} \
            --files {full_filename},.env \
            {python_file} -f {full_filename}"

        stdin, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode()
        stderr_output = stderr.read().decode()

        print(output)
        print(stderr_output)

        return stderr_output
    finally:
        client.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)

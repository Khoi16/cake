from datetime import datetime

import paramiko
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator

folder = '/opt/airflow/dags/'


def list_items():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname='192.169.135.113', port=22, username='thaiha', password='thaiha1234'
    )
    sftp = client.open_sftp()
    remote_dir = '/home/khoinkn/'
    print('list dir', sftp.listdir())

    sftp.close()
    client.close()
    
def upload_items():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname='192.169.135.113', port=22, username='thaiha', password='thaiha1234'
    )
    sftp = client.open_sftp()
    remote_dir = '/home/khoinkn/'
    for filename in os.listdir(folder):
            local_file_path = os.path.join(folder, filename)
            
            if os.path.isfile(local_file_path):
                try:
                    # Check if the file exists on the remote server
                    sftp.stat(f"{remote_dir}/{filename}")
                    print(f"Skipping '{filename}' as it already exists on the server.")
                except FileNotFoundError:
                    # Upload the file if it doesn't exist
                    print(f"Uploading '{filename}' as it does not exist on the server.")
                    sftp.put(local_file_path, f"{remote_dir}/{filename}")
    print('dir list', sftp.listdir())
    sftp.close()
    client.close()
    



with DAG(
    dag_id='test_sftp',
    start_date=datetime(2024, 10, 14),
    schedule_interval='@Hourly',
    catchup=True,
) as dag:
    task1 = PythonOperator(task_id='list_item', python_callable=list_items)
    task2 = PythonOperator(task_id = 'upload_items', python_callable = upload_items)
task1 >> task2

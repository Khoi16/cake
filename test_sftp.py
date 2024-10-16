from datetime import datetime

import paramiko
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator

folder = '/opt/airflow/dags/repo'
src='192.169.135.113'
des='192.169.89.92'
port =22
username='khoinkn'
password='khoinkn1234'
remote_dir = '/home/khoinkn/'


def list_items_src_server():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=src, port=port, username=username, password=password
    )
    sftp = client.open_sftp()
    remote_dir = dir
    list_dir = sftp.listdir()
    print('list dir on source server', sftp.listdir())

    sftp.close()
    client.close()
    return list_dir


def list_items_des_server():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=des, port=port, username=username, password=password
    )
    sftp = client.open_sftp()
    remote_dir = dir
    list_dir = sftp.listdir()
    print('list dir on destination server', list_dir)

    sftp.close()
    client.close()
    return list_dir

def check_if_exsit(src, des, port, username, password, dir):
    src_srv_files = list_items_src_server()
    des_srv_files = list_items_des_server()
    return [file for file in src_srv_files if file not in des_srv_files]

    
def upload_items_to_src_server():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=src, port=port, username=username, password=password
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

def upload_items_from_src_to_des_server():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=src, port=port, username=username, password=password
    )
    # sftp = client.open_sftp()
    remote_dir = '/home/khoinkn/'

    list_file = check_if_exsit(src, des, port, username, password, remote_dir)
    for filename in list_file:
        client.exec_command("sshpass -p \'{}\' scp {}/{} {}@{}:{}".format(password, remote_dir, filename, username, des, remote_dir))
            # local_file_path = os.path.join(folder, filename)
            
            # if os.path.isfile(local_file_path):
            #     try:
            #         # Check if the file exists on the remote server
            #         sftp.stat(f"{remote_dir}/{filename}")
            #         print(f"Skipping '{filename}' as it already exists on the server.")
            #     except FileNotFoundError:
            #         # Upload the file if it doesn't exist
            #         print(f"Uploading '{filename}' as it does not exist on the server.")
            #         sftp.put(local_file_path, f"{remote_dir}/{filename}")
    client.close()
    
with DAG(
    dag_id='sftp_tranfers_file',
    start_date=datetime(2024, 10, 15),
    schedule_interval='@Hourly',
    catchup=True,
) as dag:
    task1 = PythonOperator(task_id='list_item', python_callable=list_items_src_server)
    task2 = PythonOperator(task_id = 'upload_items_to_source_server', python_callable = upload_items_to_src_server)
    task3 = PythonOperator(task_id = 'upload_items_from_source_to_destination_server', python_callable = upload_items_from_src_to_des_server)
task1 >> task2 >> task3

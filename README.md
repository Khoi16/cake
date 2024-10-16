# cake



# Problem Statement
The task involves two SFTP destinations, referred to as <source> and <target>.
Your objective is to develop an Apache Airflow DAG that facilitates the transfer of files from the SFTP server at <source> to the SFTP server at <target> and ensures the preservation of the original directory structure.
The synchronization process should be unidirectional; hence, any modification made on <target> must not impact the <source>.
Deleted files on SFTP server at <source> must remain intact on <target> server.


## Examples:
On March 1st, 2024, when a file named sftp://<source>/a/b/c/file_1.txt is detected on the source server, it should be replicated to sftp://<target>/a/b/c/file_1.txt on the destination server.
On March 2nd, 2024, a file named sftp://<source>/a/b/c/file_2.txt appears on the source server and subsequently should be transferred to sftp://<target>/a/b/c/file_2.txt on the destination server.
On March 3rd, 2024, a file named sftp://<source>/a/b/c/file_3.txt appears on the source server and should then be transferred to sftp://<target>/a/b/c/file_3.txt on the destination server.


## Work for submiting 

1. This DAGs will check and upload file from git main branch to source server
2. Following, this will check and upload file from source server to destination server
3. Airflow has a function that can sync from git at specific branch to DAGs
4. I setup a system for showing. https://viettelflow-cc7a79f1.daasidc.org/ on cloud kubernetes
5. Username and password will be update through email.
6. DAG:  sftp_tranfers_file (sync realtime from git main)  (CI/CD for Machine Learning)
7. Src='192.169.135.113', Des='192.169.89.92' two different vm(pod) same namespace in k8s.
8. Sorry for being late


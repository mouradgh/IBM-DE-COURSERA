# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash import BashOperator
# This makes scheduling easy
import pendulum

# defining DAG arguments
default_args = {
    'owner': 'Mourad Gh',
    'start_date': pendulum.today('UTC'),
    'email': ['mou@rad.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG
dag = DAG(
    'my-first-dag',
    default_args=default_args,
    description='My first DAG',
    schedule=timedelta(days=1),
)

# Define a download task that gets a text file
download = BashOperator(
    task_id='download',
    bash_command='curl https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt > /home/mouradelghissassi/airflow/dags/web-server-access-log.txt',
    dag=dag,
)

# Define an extract task that keeps the timestamp and visitorid fields
extract = BashOperator(
    task_id='extract',
    bash_command='cut -f1,4 -d"#" /home/mouradelghissassi/airflow/dags/web-server-access-log.txt > /home/mouradelghissassi/airflow/dags/extracted.txt',
    dag=dag,
)

# Define a transform task that capitalizes the visitorid field
transform = BashOperator(
    task_id='transform',
    bash_command='tr "[a-z]" "[A-Z]" < /home/mouradelghissassi/airflow/dags/extracted.txt > /home/mouradelghissassi/airflow/dags/capitalized.txt',
    dag=dag,
)

# Define a load task that compresses the resulting file
load = BashOperator(
    task_id='load',
    bash_command='zip /home/mouradelghissassi/airflow/dags/log.zip /home/mouradelghissassi/airflow/dags/capitalized.txt' ,
    dag=dag,
)

# Create the task pipeline block
download >> extract >> transform >> load

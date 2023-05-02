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
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule=timedelta(days=1),
)

# Define an unzip task
unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='sudo tar zxvf tolldata.tgz',
    dag=dag,
)

# Define an extract task
extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -f1-4 -d"," vehicle-data.csv > csv_data.csv',
    dag=dag,
)

# Define an extract task
extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -f5-7 tollplaza-data.tsv > tsv_data.csv',
    dag=dag,
)

# Define an extract task
extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cut -b 59- payment-data.txt > fixed_width_data.csv',
    dag=dag,
)

# Define a consolidation task
consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv',
    dag=dag,
)

# Define a transformation task
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='tr "[a-z]" "[A-Z]" < extracted_data.csv > transformed_data.csv',
    dag=dag,
)

# Create the task pipeline block
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data

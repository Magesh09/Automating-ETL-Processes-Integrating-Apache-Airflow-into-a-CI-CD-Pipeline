### **Automating ETL Processes: Integrating Apache Airflow into a CI/CD Pipeline**

---

### **Index:**

1. [Introduction](#1-introduction)
2. [Problem Statement](#2-problem-statement)
3. [Prerequisites](#3-prerequisites)
4. [AWS Configuration Steps](#4-aws-configuration-steps)
5. [Step-by-Step Process](#5-step-by-step-process)
   - 5.1 [Setting Up WSL2 on Windows](#51-setting-up-wsl2-on-windows)
   - 5.2 [Installing and Configuring Apache Airflow](#52-installing-and-configuring-apache-airflow)
   - 5.3 [Creating the Unified Python Script](#53-creating-the-unified-python-script)
   - 5.4 [Creating the Bash Wrapper](#54-creating-the-bash-wrapper)
   - 5.5 [Building the Airflow DAG](#55-building-the-airflow-dag)
6. [Conclusion](#6-conclusion)

---

### 1. **Introduction**

This project demonstrates how to automate and orchestrate a complete **ETL (Extract, Transform, Load)** job for sales data using **Apache Airflow**, an open-source workflow management platform. The pipeline automates the extraction of sales data from **Amazon S3**, performs necessary transformations, and loads the transformed data into **Amazon DynamoDB**. In addition, it sends notifications through **Amazon SNS**. The entire ETL process is encapsulated in a single Python script and executed via a Bash wrapper, making it easy to maintain and scalable.

Apache Airflow acts as the scheduler, automatically managing the execution of this ETL job on specified dates, at regular intervals, and for a set number of repetitions. It provides an intuitive interface for monitoring and managing tasks, ensuring that the ETL pipeline runs efficiently and reliably.

#### Benefits of Using Apache Airflow in ETL Jobs:
- **Automation**: Automates the scheduling and execution of ETL jobs, removing manual intervention.
- **Scalability**: Easily scales to accommodate growing data and complex workflows.
- **Monitoring**: Provides robust tools to track task progress, handle errors, and retry failed tasks.
- **Flexibility**: Supports complex workflows with task dependencies, allowing seamless orchestration of multi-step ETL processes.
- **Open-Source**: As an open-source tool, Airflow is highly customizable and integrates well with a wide range of data sources and destinations.

This project showcases how Airflow can streamline and enhance the efficiency of ETL jobs, making it ideal for managing large-scale data processing.

---

### 2. **Problem Statement**

In many scenarios, organizations require running a set of tasks over a certain period on selected days and at specific times. Manually setting alarms to trigger the execution of these tasks can be cumbersome and prone to errors, leading to potential delays in data processing or analysis. Without a robust scheduling mechanism, teams face the challenge of ensuring that tasks run reliably without requiring constant oversight or manual intervention.

To solve this problem, we automate the process using the open-source workflow management software **Apache Airflow**. Airflow allows for the scheduling of ETL processes to run at specified times and intervals without manual intervention, providing an efficient solution to orchestrate complex data workflows.

---

### 3. **Prerequisites**

1. **Windows 10/11** with **WSL2** installed.
2. **Ubuntu** installed on **WSL2**.
3. **Apache Airflow**, **Python**, and **AWS CLI** installed on Ubuntu.
4. **AWS account** with **S3**, **DynamoDB**, and **SNS** configured.

---

### 4. **AWS Configuration Steps**

Before running the pipeline, you need to set up the necessary AWS services:

#### 4.1 **Creating an S3 Bucket**

1. **Log in to AWS Management Console** and navigate to the **S3** service.
2. Click on **Create bucket**.
3. **Bucket Name**: `my-sales-bucket`
4. **Region**: Select your preferred region.
5. Click on **Create bucket**.

![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/AWS_account.PNG)

#### 4.2 **Upload Sales Data to S3**

1. Navigate to the newly created bucket.
2. Click on **Upload** and add your `sales_data.csv` file containing sales data.
3. Click on **Upload** to finish.

![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/S3_file_upload.PNG)

#### 4.3 **Creating a DynamoDB Table**

1. In the AWS Management Console, navigate to **DynamoDB**.
2. Click on **Create table**.
3. **Table name**: `SalesData`
4. **Primary key**: Set `OrderID` (String).
5. Click on **Create**.

![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Dynomodb.PNG)

#### 4.4 **Creating an SNS Topic**

1. Navigate to the **SNS** service in the AWS Management Console.
2. Click on **Topics** in the left sidebar, then **Create topic**.
3. **Type**: Standard.
4. **Name**: `SalesDataNotification`.
5. Click on **Create topic** and add **Subscription email**.
6. Note the **Topic ARN**; it will be used in the Python script for sending notifications.

![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Sns_configuration.PNG)

#### 4.5 **Configuring AWS CLI**

1. Open your terminal and configure the AWS CLI with your credentials:
   ```bash
   aws configure
   ```   
![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/AWS_cli_configure.PNG)

2. Enter your **AWS Access Key ID**, **Secret Access Key**, **region**, and **output format** (e.g., `json`).

![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/AWS_Key.PNG)

---

### 5. **Step-by-Step Process**

#### 5.1 **Setting Up WSL2 on Windows**

Follow these steps to enable and set up **WSL2** and install **Ubuntu**:

1. **Open Windows Search**:
   - Press the **Windows key** or click on the **Search** icon in your taskbar.
   - Type **Turn Windows features on or off** and click on the result.

2. **Enable Windows Subsystem for Linux**:
   - In the **Windows Features** dialog box that appears, scroll down and look for **Windows Subsystem for Linux**.
   - Check the box next to it and click **OK**.
   - Allow the system to install the necessary files, then **restart** your computer if prompted.

![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Enabling_Windows_Subsystem_for_Linux.PNG)

3. **Open PowerShell as an administrator and run**:
   ```bash
   wsl --install
   ```
   This command will enable WSL and install the latest Ubuntu distribution by default. Wait for the process to complete.

4. **Restart Your Computer**:
   - After the installation is complete, **restart** your computer if required.

5. **Set up Linux Distro**:
   - Upon restarting, open **Ubuntu** from your Start menu.
   - Follow the instructions to set up your Linux username and password.

You now have WSL installed and can start using Linux on Windows!

![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Linux%20installation.PNG)

#### 5.2 **Installing and Configuring Apache Airflow**

##### Step 1: Install Dependencies
1. Update your system and install the required packages:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   sudo pip3 install virtualenv
   ```
![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Updating_packages_linux.PNG)

![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Python3_installation.PNG)

![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Installing_virenv_package.PNG)

##### Step 2: Create a Python Virtual Environment
1. Create and activate a virtual environment for Airflow:
   ```bash
   mkdir airflow_project
   cd airflow_project
   virtualenv airflow_venv
   source airflow_venv/bin/activate
   ```
![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Create_activate_venv.PNG)

##### Step 3: Install Apache Airflow
1. Install Airflow using the constraints file:
   ```bash
   AIRFLOW_VERSION=2.6.2
   PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
   CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
   pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
   ```
![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Intalling_apache_airflow.PNG)

##### Step 4: Initialize and Start Apache Airflow
1. Initialize the database:
   ```bash
   airflow db init
   ```
   ![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Initializing_sqlite_db.PNG)
   
3. Create an admin user:
   ```bash
   airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin_password
   ```
   
   ![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Adminuser_webui.PNG)
   
5. Start the Airflow services:
   ```bash
   airflow scheduler &
   airflow webserver --port 8085
   ```
   ![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/StartAirflow_schedular.PNG)
   
7. Open the Airflow web interface in your browser at `http://localhost:8085`.

   ![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/WebUI.PNG)
---

#### 5.3 **Creating the Unified Python Script**

In this section, we'll create a single Python script that handles all tasks (extracting, transforming, loading, and notifying).

##### Step 1: Create the Unified Python Script
1. Create a Python script named `sales_data_pipeline.py` in the project directory:
   ```bash
   nano sales_data_pipeline.py
   ```
2. Add the following code to handle all tasks:

```python
import boto3
import pandas as pd
import csv
import os

def extract_data():
    s3 = boto3.client('s3')
    s3.download_file('my-sales-bucket', 'sales_data.csv', '/tmp/sales_data.csv')

def transform_data():
    df = pd.read_csv('/tmp/sales_data.csv')
    df['TotalAmount'] = df['Quantity'] * df['Price']
    df.to_csv('/tmp/transformed_sales_data.csv', index=False)

def load_data():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SalesData')

    with open('/tmp/transformed_sales

_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            table.put_item(Item=row)

def send_notification():
    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:your-region:your-account-id:SalesDataNotification',
        Message='Sales data ETL process completed successfully.'
    )

if __name__ == "__main__":
    extract_data()
    transform_data()
    load_data()
    send_notification()
```

---

#### 5.4 **Creating the Bash Wrapper**

Now, create a Bash script to serve as a wrapper for the Python script.

##### Step 1: Create the Bash Wrapper
1. Create a Bash script named `run_pipeline.sh`:
   ```bash
   nano run_pipeline.sh
   ```
  
2. Add the following code to the script:

```bash
#!/bin/bash

# Activate the virtual environment
source ~/airflow_project/airflow_venv/bin/activate

# Run the Python ETL pipeline
python3 sales_data_pipeline.py
```
3. Make the script executable:
   ```bash
   chmod +x run_pipeline.sh
   ```
---

#### 5.5 **Building the Airflow DAG**

Finally, create a DAG (Directed Acyclic Graph) to automate the execution of the ETL pipeline in Airflow.

##### Step 1: Create the DAG File
1. Create a new Python file in the Airflow DAGs directory:
   ```bash
   nano ~/airflow/dags/sales_data_dag.py
   ```
2. Add the following code to define the DAG:

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 26),
    'retries': 1,
}

with DAG('sales_data_etl_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    run_etl_pipeline = BashOperator(
        task_id='run_etl_pipeline',
        bash_command='bash /path/to/your/run_pipeline.sh'
    )

    run_etl_pipeline
```
Make sure to replace `/path/to/your/run_pipeline.sh` with the actual path to your Bash script.

![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/sales_data_pipeline.PNG)

![Example Image](https://github.com/Magesh09/Automating-ETL-Processes-Integrating-Apache-Airflow-into-a-CI-CD-Pipeline/blob/main/images/Running_ETL.PNG)

---

### 6. **Conclusion**

By utilizing Apache Airflow in conjunction with AWS services, we have successfully automated the ETL process for sales data, enabling efficient data processing and management. This project highlights the ease of orchestrating complex workflows, ensuring that data pipelines can run reliably and automatically, reducing the need for manual intervention and minimizing errors.

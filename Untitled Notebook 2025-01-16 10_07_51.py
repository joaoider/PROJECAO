# Databricks notebook source
pip install DatabricksAPI

# COMMAND ----------

from databricks_api import DatabricksAPI

# Initialize the DatabricksAPI with your Databricks instance URL and token
db = DatabricksAPI(
    host='https://<your-databricks-instance>',
    token='dapi862ed10a00bea17138439d7700b5b086'
)

# Define the job ID and parameters if any
job_id = 'PROJECAO_DD_geral'

# Run the job
run_response = db.jobs.run_now(job_id=job_id)

# Display the run response
display(run_response)

# COMMAND ----------



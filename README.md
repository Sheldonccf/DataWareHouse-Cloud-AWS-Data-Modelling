# Sythesis

The created database aims at helping a startup understand its customers' preferences. 
The Startup could further recommend and customize personal playlists for each individual 
customer based on their favourite artists, songs, lengths of songs etc.
The startup could also design a better advertisement strategy based on their users' 
locations and the websites or apps through which their users log in to Sparkify.

# Table Design

The result data is organized in in the style of star schema. 
The songplay_table is the fact table and other tables are dimension tables.
The staging tables are temporary tables where source data are loaded rapidly, 
especially in a big-data scenario. Further insertions into the star schema are based on
my preliminary understanding of the samples in the staging tables.

# How to create the DataWarehouse

1. Search and create a IAM role on AWS region "US-west-2" and keep note of the KEY and SECRETE code.
2. Update the "KEY" and "SECRETE" values in "dwh.cpg".
3. Run "AWS_Redshift_Infrastructure_as_code_A" to test print the default data template in the S3 data bucket
4. Run "AWS_Redshift_Infrastructure_as_code_B" to get IAM role ARN necessary for creating the data warehouse and test connection
5. Update the "IAM role ARN" in "dwh.cpg", Define and Update the following variables yourself depending on what level of performance and pricing: CLUSTER_TYPE, NUM_NODES, NODE_TYPE, CLUSTER_IDENTIFIER, DB_NAME, DB_USER, DB_PASSWORD
6. Run "AWS_Redshift_Infrastructure_as_code_C"  and get the host address and port address of the created AWS Redshift cluster
7. Update the host and port address variable in "dwh.cpg"
8. Run "AWS_Redshift_Infrastructure_as_code_D "to open an incoming TCP portal to access the database and test the connection
9. Run "create_tables.py" to create a relational DB and staging tables.
10. Run "etl.py" to insert data to the staging tables and then the cloud relational DB.
11. Design and Run test queries to analyze the data from the Data warehouse

# Files

"dwh.cpg" file: contains the template needed for authentification creating
an AWS Redshift cluster.

"create_tables.py": functions to create Postgres tables according to a star schema 
and the staging tables.

"etl.py": implementation of etl pipelines to insert the raw data to the staging tables and 
transfer data from staging tables to the star schema.

"Infrastructure-as-codeA": using python to create an AWS Redshift cluster directly

"Infrastructure-as-codeB": using python to create an AWS Redshift cluster directly

"Infrastructure-as-codeC": using python to create an AWS Redshift cluster directly

"Infrastructure-as-codeD": using python to create an AWS Redshift cluster directly

"README.md": instructions and documentation.

"sql_queries.py": a collection of sql queries to be imported for create tables and copying
raw data to the staging tables and transfer data from staging tables to the star schema.

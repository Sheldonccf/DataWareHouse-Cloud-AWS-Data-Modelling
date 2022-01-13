# Synthesis

The created database aims at helping a startup understand its customers' preferences. 
The Startup could further recommend and customize personal playlists for each individual 
customer based on their favourite artists, songs, lengths of songs etc.
The startup could also design a better advertisement strategy based on their users' 
locations and the websites or apps through which their users log in to Sparkify.

# Data Source:

Kaggle's "Million Songs Dataset" re-organized by Udacity the educational institute.

# Table Design

The result data is organized in in the style of star schema. 
The "songplay_table" is the fact table and other tables are dimension tables.
The staging tables are temporary tables where source data are loaded rapidly, 
especially in a big-data scenario. Further insertions into the star schema (fact tables and dimension tables) are based on
my preliminary understanding of the the data types and appearances of null values in the staging tables.

# How to Create the DataWarehouse

Please follow the instructions in  "Infrastructure-as-code.ipynb" to update variable values in
"dwh.cpg" and run the cells in "Infrastructure-as-code.ipynb" from JupyterNB in sequence.

After running the last cell in "Infrastructure-as-code.ipynb", run "create_tables.py" and
"etl.py" to build the relational tables hosted on Amazon Redshift.

# Files

"dwh.cpg" file: contains the template needed for authentification creating
an AWS Redshift cluster.

"create_tables.py": functions to create Postgres tables according to a star schema 
and the staging tables.

"etl.py": implementation of etl pipelines to insert the raw data to the staging tables and 
transfer data from staging tables to the star schema.

"Infrastructure-as-code.ipynb" Instruction to create an AWS Redshift from python so that
relational tables can be hosted on the cloud and data loaded onto the tables.

"README.md": instructions and documentation.

"sql_queries.py": a collection of sql queries to be imported for create tables and copying
raw data to the staging tables and transfer data from staging tables to the star schema.

import AWS_Redshift_Infrastructure_as_code_A
import AWS_Redshift_Infrastructure_as_code_B

# Create the AWS Redshift Cluster and customize the cluster type, DB name and passoword
# use the roleArn authentification code to establish connection between this Redshift
# DataWarehouse and the S3 data source bucket
try:
    response = redshift.create_cluster(        
        #HW
        ClusterType=CLUSTER_TYPE,
        NodeType=NODE_TYPE,
        #NumberOfNodes=int(NUM_NODES),
        
        #Identifiers & Credentials
        DBName=DB_NAME,
        ClusterIdentifier=CLUSTER_IDENTIFIER,
        MasterUsername=DB_USER,
        MasterUserPassword=DB_PASSWORD,
        
        #Roles (for s3 access)
        IamRoles=[roleArn]
         
    )
except Exception as e:
    print(e)

#print and verify the attributes of the created DataWarehouse
def prettyRedshiftProps(props):
    pd.set_option('display.max_colwidth', -1)
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])

myClusterProps = redshift.describe_clusters(ClusterIdentifier=CLUSTER_IDENTIFIER)['Clusters'][0]
prettyRedshiftProps(myClusterProps)

# Get the Endpoint(Host Address of the created DataWarehouse)
DWH_ENDPOINT = myClusterProps['Endpoint']['Address']
DWH_ROLE_ARN = myClusterProps['IamRoles'][0]['IamRoleArn']
print("DWH_ENDPOINT :: ", DWH_ENDPOINT)
print("DWH_ROLE_ARN :: ", DWH_ROLE_ARN)


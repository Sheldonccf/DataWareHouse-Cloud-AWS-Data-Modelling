import AWS_Redshift_Infrastructure_as_code_A
import AWS_Redshift_Infrastructure_as_code_B
import AWS_Redshift_Infrastructure_as_code_C
#Opening an incoming TCP portal to access the endpoint
try:
    vpc = ec2.Vpc(id=myClusterProps['VpcId'])
    defaultSg = list(vpc.security_groups.all())[0]
    print(defaultSg)
    
    defaultSg.authorize_ingress(
        GroupName= 'default',
        CidrIp='0.0.0.0/0', 
        IpProtocol='TCP',  
        FromPort=int(DB_PORT),
        ToPort=int(DB_PORT)
    )
except Exception as e:
    print(e)
    
#Test Connection to the created cluster
%load_ext sql
import psycopg2
conn_string="postgresql://{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWORD, DWH_ENDPOINT, DB_PORT,DB_NAME)
print(conn_string)
%sql $conn_string

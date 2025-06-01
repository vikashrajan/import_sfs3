----------------Create S3 bucket to save xml data ------------------------------------------
Create a s3 bucket in aws name as  xml-data-source-0001
 
Uncheck Block Public Access settings for this bucket.
Create bucket
 ![image](https://github.com/user-attachments/assets/8f8bb7e5-1f9f-4b37-b4c5-81adbecef401)
![image](https://github.com/user-attachments/assets/96f04b59-cb96-4164-a5b7-0ef326864a5b)

Now need to create IAM user for accessing the s3 bucket via code
1.Go to IAM Console: https://console.aws.amazon.com/iam/
•  Choose Users from the left-hand menu.
• 	“Add user” to create a new one
2  Enable Programmatic Access
•	When creating or editing the user, ensure “Programmatic access” is selected.
•	This will generate:
o	aws_access_key_id
o	aws_secret_access_key
3. Attach S3 Permissions
You can attach:
•	AmazonS3FullAccess (for full access)
•	Or a custom policy for specific access
 
![image](https://github.com/user-attachments/assets/36843a09-e6eb-4cd1-be74-4e28b3ad0488)

 
![image](https://github.com/user-attachments/assets/117c8c3f-7731-4039-bebe-eaad369b0194)


![image](https://github.com/user-attachments/assets/beb8b0ab-19cd-472e-89f4-4bd54cfdd493)

 
Add a role AmazonS3FullAccess to the create user as below .
 ![image](https://github.com/user-attachments/assets/c21f0df6-2290-4387-bad9-6ff9d19a52d0)

Download the access key for further use in code.
Create data generator code to generate the data load into s3  bucket
Open VS Code and create a new folder called:
import_sfs3

 ![image](https://github.com/user-attachments/assets/66658ae7-262f-414a-b20b-58987e4503ae)

Inside VS Code terminal, initialize a virtual environment:
python -m venv venv
venv\Scripts\activate  # On Windows
 
![image](https://github.com/user-attachments/assets/07a98ab8-e084-41b4-87ce-0f9e03725200)

Create a file named requirements.txt in the root of your project folder with the following content:
 ![image](https://github.com/user-attachments/assets/ba532eaa-4cdc-4cd5-bce7-70032fcc7ba0)

Install all dependencies from it:
pip install -r requirements.txt
 ![image](https://github.com/user-attachments/assets/76906389-c6c2-4cf7-bd10-dca8400f7ec5)


Create a python file generatedata.py.
 ![image](https://github.com/user-attachments/assets/44144427-ac57-4645-8222-048f46be0c0c)


Create a python file upload_to_s3.py.
 ![image](https://github.com/user-attachments/assets/f1c098ee-c3af-4a26-9f4c-1196e5c333f2)

Create a python file  venv\aws_config.py
The above generatedata.py file will save data in local folder and upload the data in s3 buckets as per the below screen shots
 ![image](https://github.com/user-attachments/assets/d87f05dd-fda1-4025-84fd-1af8db73ba7f)

Enter the total records do you want to generate: 10
Enter the file size in MB, Do you want to generate: 1
Enter the output folder path to save JSON files: D:\Projects\import_sfs3\data
Once the files are uploaded on the S3 buckets lambda function will be triggered and save the data into Snowflake data base.

 ![image](https://github.com/user-attachments/assets/c5f476ff-c8c2-4492-9a55-5295108ad06c)

Git hub code vikashrajan/import_sfs3


-Create lambda function to save the data in snowflake DB-----------------------
Create Lambda functions and add trigger 
 
 ![image](https://github.com/user-attachments/assets/36e08b9d-1828-4167-ae05-9974c42bb472)
![image](https://github.com/user-attachments/assets/f0346db8-58b5-44f6-8965-e5aa43d7143e)

Add trigger with below details as created earlier steps.
 ![image](https://github.com/user-attachments/assets/9ee7f937-aa8e-4a9a-83cb-1135e8955116)

Add environment variable as below
 
 ![image](https://github.com/user-attachments/assets/4ba527c7-79f8-42a7-a330-a237c8105f01)

![image](https://github.com/user-attachments/assets/9b9db89c-3f87-42dd-b44e-8ef262238873)

Add code as per this git hub url 

-Create database and table in snowflake DB as per the below script-----------------------
CREATE OR REPLACE DATABASE DEMO_DB;

-- Create schema (optional, can use default)
CREATE OR REPLACE SCHEMA DEMO_DB.PUBLIC;
USE DATABASE DEMO_DB;
USE SCHEMA PUBLIC;



CREATE OR REPLACE TABLE parsed_data (
    id      INT AUTOINCREMENT PRIMARY KEY,
    name    STRING,
    phone   STRING,
    address STRING,
    email   STRING
);



# AWS\_Billing_Notification
Collect AWS Billing statistics of multiple AWS accounts for last month, and send email to related division.

## Description
This script can collect estimated charges statistics from CloudWatch to calculate the total cost of each account, and sent subtotal for every departments.

## Setup
1. Install [Amazon CloudWatch Command Line Tool](https://aws.amazon.com/developertools/2534)
2. Modify "AWS\_CW\_HOME" in get_billing.py, set the path to where you "install Amazon CloudWatch Command Line Tool". 
3. Modify mailing settings in get_billing.py: "mailServer", "fromAddr", "ccAddrs".
4. Modify department informations in get_billing.py: Department code, name and email list.
5. In IAM, create user with CloudWatch ReadOnly permission, and get the Access Key and Secret Key. Do this action for each AWS account you want to collect.
6. Modify AWS account information in get_billing.py using the Keys got in last step.
7. If you want to use crontab to run this script, modify "JAVA\_HOME", "AWS\_CLOUDWATCH\_HOME" and path to logs in cron\_get\_billing.sh .

## Usage
* Because of AWS use GMT to calculate date, please determine the time you run this script. The better time to run is 2nd of the month.
* You can run get_billing.py manually, without any argument.
* Or you can set crontab to run cron_get_billing.sh automatically.

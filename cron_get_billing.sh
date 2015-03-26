#!/bin/sh
export JAVA_HOME="/Path/To/jvm/jre-1.7.0-openjdk.x86_64"
export AWS_CLOUDWATCH_HOME="/Path/To/CloudWatch-1.0.20.0"

/usr/bin/python /Path/To/get_billing.py > /Path/To/aws_billing.log 2> /Path/To/aws_billing.err


"""
this file reads from continuum.yaml and makes key settings available
as python objects to some other scripts via import, it is purely
a convinience function.
"""
import yaml
ontinuum = "continuum.yaml"

with open(ontinuum, 'r') as f:
    doc = yaml.load(f)


http_user = doc["http_auth"]["user"]
http_password = doc["http_auth"]["password"]
crazy_user = doc["http_auth"]["crazy_user"]
crazy_password = doc["http_auth"]["crazy_password"]
web_user = doc["http_auth"]["web_user"]
web_password = doc["http_auth"]["web_password"]

bot_aws_user = doc["elife_bot_user_aws"]["aws_username"]
bot_aws_key = doc["elife_bot_user_aws"]["key"]
bot_aws_secret = doc["elife_bot_user_aws"]["secret"]

dashboard_aws_user = doc["elife_dashboard_user_aws"]["aws_username"]
dashboard_aws_key = doc["elife_dashboard_user_aws"]["key"]
dashboard_aws_secret = doc["elife_dashboard_user_aws"]["secret"]

builder_path = doc["builder_path"]
builder_private_path = doc["builder_private_path"]
prefix = doc["prefix"]
domain_name = doc["domain_name"].values()[0]
region = doc["aws_region"].values()[0]
queue_map = doc["sqs_queues"]
s3_buckets = doc["s3_buckets"]
s3_protected_buckets = doc["s3_protected_buckets"]
protected_prefixes = doc["protected_prefixes"]

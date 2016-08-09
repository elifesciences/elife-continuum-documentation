"""
this file reads from continuum.yaml and makes key settings available
as python objects to some other scripts via import, it is purely
a convinience function.
"""
import yaml
ontinuum = "continuum.yaml"

with open(ontinuum, 'r') as f:
    doc = yaml.load(f)


dashboard_user = doc["http_auth"]["user"]
dashboard_password = doc["http_auth"]["password"]
crazy_user = doc["http_auth"]["crazy_user"]
crazy_password = doc["http_auth"]["crazy_password"]
web_user = doc["http_auth"]["web_user"]
web_password = doc["http_auth"]["web_password"]

bot_aws_user = doc["elife_bot_user_aws"]["aws_username"]
bot_aws_key = doc["elife_bot_user_aws"]["key"]
bot_aws_secret = doc["elife_bot_user_aws"]["secret"]

# dashboard_aws_user = doc["elife_dashboard_user_aws"]["aws_username"]
# dashboard_aws_key = doc["elife_dashboard_user_aws"]["key"]
# dashboard_aws_secret = doc["elife_dashboard_user_aws"]["secret"]

scheduler_db_username = doc["elife_scheduler_other"]["db_username"]
scheduler_db_password = doc["elife_scheduler_other"]["db_password"]
scheduler_app_secret = doc["elife_scheduler_other"]["app_key"]

builder_path = doc["builder_path"]
builder_private_path = doc["builder_private_path"]
builder_private_repo = doc["builder_private_repo"]

prefix = doc["prefix"]
swf_domain = doc["swf_domain"].values()[0]
domain_name = doc["domain_name"].values()[0]


region = doc["aws_region"].values()[0]
queue_map = doc["sqs_queues"]
s3_buckets = doc["s3_buckets"]
s3_protected_buckets = doc["s3_protected_buckets"]
s3_protected_queues = doc["sqs_protected_queues"]
protected_prefixes = doc["protected_prefixes"]

# Drupal
drupal_hostname  = doc["drupal_site_details"]["hostname"]
drupal_update_user = doc["drupal_site_details"]["update_user"]
drupal_update_pass = doc["drupal_site_details"]["update_pass"]
drupal_website_username = doc["drupal_site_details"]["drupal_website_username"]
drupal_db_username = doc["drupal_site_details"]["drupal_db_username"]
drupal_user_username = doc["drupal_site_details"]["drupal_user_username"]
drupal_db_password = doc["drupal_site_details"]["drupal_db_password"]
drupal_db_test_password = doc["drupal_site_details"]["drupal_db_test_password"]
drupal_user_password = doc["drupal_site_details"]["drupal_user_password"]

# lax app credentials
lax_app_secret = doc["lax_application"]["app_secret"]
lax_db_username = doc["lax_application"]["db_username"]
lax_db_password =  doc["lax_application"]["db_password"]

# deploy email
deploy_email = doc["application_emails"]["deploy_user_email"]

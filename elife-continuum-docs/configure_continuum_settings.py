import sys
import os
import boto3
import ruamel.yaml # ruamel preserves yaml order and comments
from aws_setting_utils import s3_buckets, prefix, region, queue_map, builder_path, builder_private_path
from aws_setting_utils import http_user, http_password, crazy_user, crazy_password, web_user, web_password
from aws_setting_utils import bot_aws_user, bot_aws_key, bot_aws_secret
from aws_setting_utils import dashboard_aws_user, dashboard_aws_key, dashboard_aws_secret

# AWS contstnats that have to be looked up in the AWS console (for now).


config = {"elife":"projects/elife.yaml"}

private_config = {
    "bot":"salt/elife-bot/config/opt-elife-bot-settings.py",
    "dashboard":"salt/elife-dashboard/config/srv-app-dashboard-master_settings.py",
    "scheduler":"salt/elife-dashboard/config/srv-elife-article-scheduler-src-core-master_settings.py","elife":"pillar/elife.sls",
    "dashboard_private": "pillar/elife-dashboard.sls"
    }

def set_config_paths(config, private_config, builder_path, builder_private_path):
    """
    hook up the actual location of the config files, based on our continuum config
    """
    new_config = {}
    new_private_config = {}
    for key in config.keys():
        new_config[key] = builder_path + "/" + config[key]
    for key in private_config.keys():
        new_private_config[key] = builder_private_path + "/" + private_config[key]
    return new_config, new_private_config

def check_config_files_existence(config):
    for path in config.values():
        print "checking for existence of: " + path
        try:
            f = open(path, "r")
            f.close()
            print "file found"
        except:
            print "not found: " + path

def get_yaml(path):
    with open(path, 'r') as f:
        yaml_content = ruamel.yaml.load(f, ruamel.yaml.RoundTripLoader)
    return yaml_content

def write_yaml(yaml_content, path):
    print ruamel.yaml.dump(yaml_content, Dumper=ruamel.yaml.RoundTripDumper)

# def update_yaml_file(path, key_list, new_value):
# TODO: figure out how to access and update an arbitrary value in a nested ordered dict.
#     with open(path, 'r') as f:
#         yaml_content = ruamel.yaml.load(f, ruamel.yaml.RoundTripLoader)
#
#     value = yaml_content
#     for key in key_list:
#         new_value = value[k]
#         value = new_value
#         attribute_ i, value

def set_element_in_python_settings(value, line_identifiers, settings_file):
    lines = open(settings_file, "r").readlines()
    new_file = []
    for line in lines:
        for setting_string in line_identifiers:
            if line.find(setting_string) > -1:
                line = "".join(line.split("=")[:-1]) + " = " + value
                print line
        new_file.append(line)
    print new_file
    # open(settings_file, "w").writelines(new_file)

def set_region_in_python_settings(region, settings_file):
    line_identifiers = ["simpledb_region","ses_region","sqs_region"]
    value = region
    set_element_in_python_settings(value, line_identifiers, settings_file)

def set_aws_region(region, elife_global_yaml, python_settings):
    elife_global_yaml_content = get_yaml(elife_global_yaml)
    elife_global_yaml_content["defaults"]["aws"]["region"] = region

    write_yaml(elife_global_yaml_content, elife_global_yaml)

    for py_setting in python_settings:
        set_region_in_python_settings(region, py_setting)

def set_dashboard_basic_auth(http_user, http_password, dashboard_private_yaml):
    dashboard_yaml_content = get_yaml(dashboard_private_yaml)

    dashboard_yaml_content["elife_dashboard"]["basic_auth"]["username"] = http_user
    dashboard_yaml_content["elife_dashboard"]["basic_auth"]["password"] = http_password
    write_yaml(dashboard_yaml_content, dashboard_private_yaml)

def set_web_basic_auth(http_user, http_password, elife_yaml):
    elife_yaml_content = get_yaml(elife_private_yaml)

    elife_yaml_content["elife"]["web_users"][""]["username"] = http_user
    elife_yaml_content["elife"]["web_users"][""]["password"] = http_password
    write_yaml(elife_yaml_content, elife_yaml)


def set_lax_basic_auth(http_user, http_password, elife_yaml, bot_py):
    elife_yaml_content = get_yaml(elife_private_yaml)

    elife_yaml_content["elife"]["web_users"]["crazy-"]["username"] = http_user
    elife_yaml_content["elife"]["web_users"]["crazy-"]["password"] = http_password
    write_yaml(elife_yaml_content, elife_yaml)

    # set_element_in_python_settings(value, line_identifiers, bot_py):

def set_dashboard_aws_credentials(user, key, secret, dashboard_private_yaml):
    dashboard_yaml_content = get_yaml(dashboard_private_yaml)

    dashboard_yaml_content["elife_dashboard"]["aws"]["username"] = user
    dashboard_yaml_content["elife_dashboard"]["aws"]["access_id"] = key
    dashboard_yaml_content["elife_dashboard"]["aws"]["secret_access_key"] = secret
    write_yaml(dashboard_yaml_content, dashboard_private_yaml)


def set_lax_endpoint(lax_endpoint, bot_py):
    value = lax_endpoint
    # set_element_in_python_settings(lax_endpoint, line_identifiers, bot_py)

def derive_lax_endpoint_from_domain(domain):
    instance_name = raw_input("what is your lax instance name?")
    lax_server = instance_name + "--lax." + domain
    lax_update = lax_server + "/api/v1/article/create-update/"
    lax_article_versions = lax_server + "api/v1/article/10.7554/eLife.{article_id}/version/"
    return lax_update, lax_article_versions

if __name__ == "__main__":
    config, private_config = set_config_paths(config, private_config, builder_path, builder_private_path)
    check_config_files_existence(config)
    check_config_files_existence(private_config)

    elife_global_yaml = config["elife"]
    elife_private_yaml = private_config["elife"]
    dashboard_private_yaml = private_config["dashboard_private"]
    bot_py = private_config["bot"]
    dashboard_py = private_config["dashboard"]
    scheduler_py = private_config["scheduler"]

    set_aws_region(region, elife_global_yaml, python_settings=[bot_py, dashboard_py, scheduler_py])

    set_dashboard_basic_auth(http_user, http_password, dashboard_private_yaml)
    set_lax_basic_auth(crazy_user, crazy_password, elife_private_yaml, bot_py)
    set_web_basic_auth(web_user, web_password, elife_private_yaml) # TODO: check if the implied wildchard in the elife.sls file causes this parser to output a `?`, and whether that is going to cause a problem.

    set_dashboard_aws_credentials(dashboard_aws_user, dashboard_aws_key, dashboard_aws_secret, dashboard_private_yaml)

    # # the following all affect buider/projects/elife.yaml
    # # ideally we should be able to find out these details via the AWS API
    # set_vpc_id
    # set_subnet_id
    # set_private_formula_repo
    # set_domain_sub_domain
    #
    # # set email for let's encrypt
    #
    # # turn off write keyparis
    # turn_off_write_keyparis
    #
    # # point bot to lax server
    # lax_update, lax_versions = derive_lax_endpoint_from_domain(domain)
    # set_lax_update(lax_update, bot_py)
    # set_lax_versions(lax_versions, bot_py)
    #
    # # set lax API credentials





#
# # Read in the elife.yaml file from builder/projects/elife.yaml
# # this sets global AWS configuration
# continuum_yaml = "elife.yaml"
# with open(continuum_yaml, 'r') as f:
#     config = ruamel.yaml.load(f, ruamel.yaml.RoundTripLoader)
#
# print config["defaults"]["aws"]["region"]
#
# config["defaults"]["aws"]["region"] = region
#
# print ruamel.yaml.dump(config, Dumper=ruamel.yaml.RoundTripDumper)
#

# route = boto3.client('route53')
#
# response = route.list_hosted_zones()
# print response
#
#
# response = route.get_hosted_zone(Id="Z7QPXQ3KTRH3W")
# print response
#
# location = "us-east-1"
#
# # S3 info derioved from bot settings,
# # https://github.com/elifesciences/builder/blob/master/salt/salt/elife-bot/config/opt-elife-bot-settings.py#L25-L27
#
# required_buckets = {"production_bucket" : 'elife-production-final',
#                     "eif_bucket" : 'elife-publishing-eif',
#                     "expanded_bucket" : 'elife-publishing-expanded',
#                     "ppp_cdn_bucket" : 'elife-publishing-cdn',
#                     "archive_bucket" : 'elife-publishing-archive',
#                     "xml_bucket" : 'elife-publishing-xml'}
#
# # queue info derioved from dashboard settings, and bot settings,
# # e.g. https://github.com/elifesciences/builder/blob/master/salt/salt/elife-dashboard/config/srv-app-dashboard-prod_settings.py#L9-L11
# # https://github.com/elifesciences/builder/blob/master/salt/salt/elife-bot/config/opt-elife-bot-settings.py#L25-L27
# required_queues = {"S3_monitor_queue" : 'incoming-queue',
#                     "event_monitor_queue" : 'event-property-incoming-queue',
#                     "workflow_starter_queue" : 'workflow-starter-queue'}
#
# def set_notification_on_bucket(bucket_name):
#     bucket_notification = s3.BucketNotification('bucket_name')
#
# def create_bucket(s3, bucket_name, location):
#     print bucket_name, location
#     if location == "us-east-1":
#         s3.create_bucket(Bucket=bucket_name)
#     else:
#         s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': location})
#     return True
#
# def get_prefixed_buckets(s3, prefix):
#     prefixed_buckets = []
#     for bucket in s3.buckets.all():
#         bucket_name = bucket.name
#         if bucket_name.find(prefix + "-") > -1:
#             prefixed_buckets.append(bucket)
#     return prefixed_buckets
#
# def delete_prefixed_buckets(prefix):
#     if prefix not in allowed_deletion_prefixes:
#         raise ValueError("you are not allowed to delete that bucket")
#     prefixed_buckets = get_prefixed_buckets(prefix)
#     print "I may try to delete these buckets ", prefixed_buckets
#     for bucket in prefixed_buckets: delete_bucket(bucket)
#     return True
#
# def create_prefixed_buckets(s3, prefix):
#     for bucket in required_buckets.values():
#         create_bucket(s3, prefix + "-" + bucket, location)
#
# def create_prefixed_queues(prefix):
#     for queue in required_queues.values():
#         sqs.create_queue(QueueName=prefix + "-" + queue)
#
# def create_prefixed_swf_domain(prefix):
#     swf.register_domain(name="Publish" + "." + prefix, description="test SWF domain for thie postfixed namespace", workflowExecutionRetentionPeriodInDays="90")
#
# def create_bot_aws_resources(prefix):
#     # create_prefixed_queues(prefix)
#     create_prefixed_swf_domain(prefix)
#     # create_prefixed_buckets(prefix)
#
# def set_bucket_notification():
#     bucket_notification = s3.BucketNotification('bucket_name')
#     bucket_notification.put(QueueConfigurations[QueueArn:])
#
# def set_queue_notification(queue_arn):
#     bucket_notification = s3.BucketNotification('ct-elife-production-final')
#     print bucket_notification.__dict__
#     data = {}
#     # for valid event types see  http://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html#supported-notification-event-types
#     data['QueueConfigurations'] = [
#                 {
#                     'QueueArn': queue_arn,
#                     'Events': ["s3:ObjectCreated:*"]
#                     }
#                 ]
#
#     response = bucket_notification.put(NotificationConfiguration=data)
#     print response
#
# def get_queue_arn(prefix):
#     queues = sqs.list_queues()["QueueUrls"]
#     for queue in queues:
#         queue_simple_name = queue.split("/")[-1]
#         if queue_simple_name == prefix + "-incoming-queue":
#             queue_attributes = sqs.get_queue_attributes(QueueUrl=queue, AttributeNames=["QueueArn", "Policy"])
#             queue_arn = queue_attributes["Attributes"]["QueueArn"]
#     return queue_arn
#
# def generate_bucket_arn_from_name(bucket_name):
#     """
#     the bucket arn that we require for setting a policy on an SQS queue can be
#     derived directly from the bucket name, meaning we do not need to make
#     any calls to AWS to obtain this if we already have the bucket name.
#
#     >>> generate_bucket_arn_from_name(name)
#     arn:aws:s3:*:*:name
#     """
#     return "arn:aws:s3:*:*:" + bucket_name
#
# def generate_sqs_policy(sqs_arn, bucket_arn):
#     policy_doc =  """  {
#         "Version": "2012-10-17",
#         "Id": "%s/SQSDefaultPolicy",
#         "Statement": [
#           {
#             "Sid": "",
#             "Effect": "Allow",
#             "Principal": {
#               "AWS": "*"
#             },
#             "Action": "SQS:SendMessage",
#             "Resource": "%s",
#             "Condition": {
#               "ArnLike": {
#                 "aws:SourceArn": "%s"
#               }
#             }
#           }
#         ]
#       }
#       """ % (sqs_arn,sqs_arn, bucket_arn)
#     return policy_doc
#
# def generate_sqs_policy_json(sqs_arn, bucket_arn):
#     policy_doc = {  "Version": "2012-10-17",
#                     "Id": sqs_arn+"/SQSDefaultPolicy",
#                     "Statement": [
#                           {
#                             "Sid": "",
#                             "Effect": "Allow",
#                             "Principal": {
#                               "AWS": "*"
#                             },
#                             "Action": "SQS:SendMessage",
#                             "Resource": sqs_arn,
#                             "Condition": {
#                                 "ArnLike": {
#                                 "aws:SourceArn": bucket_arn
#                                 }
#                             }
#                         }
#                     ]
#                 }
#     return policy_doc
#
# def set_queue_policy(prefix):
#     queues = sqs.list_queues()["QueueUrls"]
#     for queue in queues:
#         queue_simple_name = queue.split("/")[-1]
#         if queue_simple_name == prefix + "-incoming-queue":
#             bucket_arn = generate_bucket_arn_from_name("ct-elife-production-final")
#             sqs_arn = get_queue_arn(prefix)
#             policy = generate_sqs_policy(sqs_arn, bucket_arn)
#             response = sqs.set_queue_attributes(QueueUrl=queue, Attributes={"Policy":policy})
#             print response
#
# if __name__ == "__main__":
#     # TODO: figure out the difference between boto3.resource and boto3.client for this code
#     s3 = boto3.resource('s3')
#     sqs = boto3.client('sqs')
#     swf = boto3.client('swf')
#
#     args = parser.parse_args()
#     prefix = args.prefix
#
#     aws_arn = generate_bucket_arn_from_name("ct-elife-production-final")
#     sqs_arn = get_queue_arn(prefix)
#     policy = generate_sqs_policy(sqs_arn, aws_arn)
#     print policy
#     policy_json = generate_sqs_policy_json(sqs_arn, aws_arn)
#     print policy_json
#     # set_queue_policy(prefix)
#     # bucket_arn = get_bucket_arn(prefix)
#     queue_arn = get_queue_arn(prefix)
#     set_queue_notification(queue_arn)

import sys
import os
import boto3
import ruamel.yaml # ruamel preserves yaml order and comments
from ruamel.yaml import dump as MyDump
from aws_setting_utils import s3_buckets, prefix, region, queue_map, builder_path, builder_private_path
from aws_setting_utils import dashboard_user, dashboard_password, crazy_user, crazy_password, web_user, web_password
from aws_setting_utils import bot_aws_user, bot_aws_key, bot_aws_secret, domain_name
from aws_setting_utils import builder_private_repo
from aws_setting_utils import drupal_hostname, drupal_update_user, drupal_update_pass, drupal_db_username, drupal_db_password, drupal_website_username, drupal_db_test_password, drupal_user_password
from aws_setting_utils import lax_app_secret, lax_db_username, lax_db_password
from aws_setting_utils import deploy_email
from aws_setting_utils import scheduler_app_secret, scheduler_db_username, scheduler_db_password

# ruamel.yaml.representer.RoundTripRepresenter.add_representer(
#     type(None),
#     lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', None)
#   )

# AWS contstnats that have to be looked up in the AWS console (for now).
# This data is not confidentail, as use of if is only possible with AWS keys
VPC_ID = "vpc-77f82b1e"
SUBNET_CIDR = "172.31.0.0/20"
SUBNET_ID_A = "subnet-afc96ec6"
SUBNET_ID_B = "subnet-cb2ee9b0"
MACHINE_AMI = "ami-9cee02f3"
RDS_SUBNETS = [SUBNET_ID_A, SUBNET_ID_B]
CDN_DISTRIBUTION_ID = "test dist id"
CDN_DOMAIN_NAME = "test cdn domain name"
LENS_CDN_DISTRIBUTION_ID = "test lens cdn dist id"
LENS_CDN_DOMAIN_NAME = "test cdn domain name"


CONFIG = {"elife":"projects/elife.yaml"}

PRIVATE_CONFIG = {
    "bot":"salt/elife-bot/config/opt-elife-bot-settings.py",
    "dashboard":"salt/elife-dashboard/config/srv-app-dashboard-master_settings.py",
    "scheduler":"salt/elife-dashboard/config/srv-elife-article-scheduler-default_settings.py",
    "dashboard_yaml": "pillar/elife-dashboard.sls",
    "elife":"pillar/elife.sls",
    "lax": "pillar/lax.sls",
    "website": "pillar/elife-website.sls"
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
    print "writing " + path
    yaml_content = ruamel.yaml.dump(yaml_content, Dumper=ruamel.yaml.RoundTripDumper, indent=4)
    new_yaml = yaml_content.replace(" -", "     -")
    new_yaml_two = new_yaml.replace("-   ", "- ")
    target = open(path,"w")
    target.write(new_yaml_two)
    target.close()

def set_element_in_python_settings(value, line_identifiers, settings_file):
    lines = open(settings_file, "r").readlines()
    new_file = []
    for line in lines:
        for setting_string in line_identifiers:
            if line.find(setting_string) > -1:
                line = "".join(line.split("=")[:-1]) + " = " + '"' + value + '"' + "\n"
                # print line
        new_file.append(line)
    new_file_content = "".join(new_file)
    target = open(settings_file,"w")
    target.write(new_file_content)
    target.close()

def set_workflow_queue_in_python_settings(value, settings_file):
    print "setting " + value + " in " + settings_file
    line_identifiers = ["workflow_starter_queue"]
    set_element_in_python_settings(value, line_identifiers, settings_file)

def set_event_queue_in_python_settings(value, settings_file):
    print "setting " + value + " in " + settings_file
    line_identifiers = ["event_monitor_queue"]
    set_element_in_python_settings(value, line_identifiers, settings_file)

def set_base_url_in_python_settings(value, settings_file):
    print "setting " + value + " in " + settings_file
    line_identifiers = ["preview_base_url"]
    set_element_in_python_settings(value, line_identifiers, settings_file)

def set_region_in_python_settings(value, settings_file):
    """
    targets settings.py in elife-bot
    and salt/elife-dashboard/config/srv-app-dashboard-master_settings.py
    in builder private
    """
    print "setting " + value + " in " + settings_file
    line_identifiers = ["simpledb_region", "ses_region", "sqs_region", "rds_region"]
    set_element_in_python_settings(value, line_identifiers, settings_file)

def set_aws_region(value, elife_global_yaml, python_settings):
    print "setting " + value + " in " + elife_global_yaml
    elife_global_yaml_content = get_yaml(elife_global_yaml)
    elife_global_yaml_content["defaults"]["aws"]["region"] = value
    write_yaml(elife_global_yaml_content, elife_global_yaml)
    for py_setting in python_settings:
        set_region_in_python_settings(value, py_setting)

def set_dashboard_basic_auth(http_user, http_password, dashboard_private_yaml):
    dashboard_yaml_content = get_yaml(dashboard_private_yaml)
    dashboard_yaml_content["elife_dashboard"]["basic_auth"]["username"] = http_user
    dashboard_yaml_content["elife_dashboard"]["basic_auth"]["password"] = http_password
    write_yaml(dashboard_yaml_content, dashboard_private_yaml)

def set_web_basic_auth(http_user, http_password, elife_yaml):
    elife_yaml_content = get_yaml(elife_private_yaml)
    elife_yaml_content["elife"]["web_users"]["default"]["username"] = http_user
    elife_yaml_content["elife"]["web_users"]["default"]["password"] = http_password
    write_yaml(elife_yaml_content, elife_yaml)

def set_lax_basic_auth(http_user, http_password, elife_yaml, elife_py):
    yaml_content = get_yaml(elife_yaml)
    yaml_content["elife"]["web_users"]["crazy-"]["username"] = http_user
    yaml_content["elife"]["web_users"]["crazy-"]["password"] = http_password
    write_yaml(yaml_content, elife_yaml)
    line_identifiers = ["lax_update_user"]
    value = http_user
    set_element_in_python_settings(value, line_identifiers, elife_py)
    line_identifiers = ["lax_update_pass"]
    value = http_password
    set_element_in_python_settings(value, line_identifiers, elife_py)

def set_dashboard_aws_credentials(user, key, secret, yaml_file):
    """
    targets the private yaml file for the dashboard
    sets that AWS credentials, most important one to keep secret
    """
    yaml_content = get_yaml(yaml_file)
    yaml_content["elife_dashboard"]["aws"]["username"] = user
    yaml_content["elife_dashboard"]["aws"]["access_id"] = key
    yaml_content["elife_dashboard"]["aws"]["secret_access_key"] = secret
    write_yaml(yaml_content, yaml_file)

def set_lax_update(lax_endpoint, bot_py):
    value = lax_endpoint
    line_identifiers = ["lax_article_versions"]
    set_element_in_python_settings(lax_endpoint, line_identifiers, bot_py)

def set_lax_versions(lax_endpoint, bot_py):
    value = lax_endpoint
    line_identifiers = ["lax_update"]
    set_element_in_python_settings(lax_endpoint, line_identifiers, bot_py)

def derive_lax_endpoint_from_domain(domain, instance_name):
    lax_server = instance_name + "--lax." + domain
    lax_update = lax_server + "/api/v1/article/create-update/"
    lax_article_versions = lax_server + "api/v1/article/10.7554/eLife.{article_id}/version/"
    print "lax update endpoint: " + lax_update
    print "lax article versions endpoint: " + lax_article_versions
    return lax_update, lax_article_versions

def set_vpc_id(value, yaml_file):
    yaml_content = get_yaml(yaml_file)
    yaml_content["defaults"]["aws"]["vpc-id"] = value
    write_yaml(yaml_content, yaml_file)

def set_ami(value, yaml_file):
    yaml_content = get_yaml(yaml_file)
    yaml_content["defaults"]["aws"]["ami"] = value
    write_yaml(yaml_content, yaml_file)

def set_subnet_id(value, yaml_file):
    """
    targets builder/projects/elife.yaml with the subnet_id value
    """
    yaml_content = get_yaml(elife_global_yaml)
    yaml_content["defaults"]["aws"]["ami"] = value
    write_yaml(yaml_content, yaml_file)

def set_subnet_cidr(value, yaml_file):
    """
    targets builder/projects/elife.yaml with the cidr value
    """
    yaml_content = get_yaml(elife_global_yaml)
    yaml_content["defaults"]["aws"]["subnet-cidr"] = value
    write_yaml(yaml_content, yaml_file)

def set_rds_subnets(value, yaml_file):
    """
    targets builder/projects/elife.yaml
    """
    print "setting rds subnet " + str(value)
    yaml_content = get_yaml(yaml_file)
    yaml_content["defaults"]["aws"]["rds"]["subnets"] = value
    write_yaml(yaml_content, yaml_file)

def set_cidr_ip(value, yaml_file):
    """
    targets builder/projects/elife.yaml with cidr_ip
    """

    new_ports = [22, {4506: {"cidr-ip": value}}, {4505: {"cidr-ip": value}} ]

    print "setting cidr_ip " + value
    yaml_content = get_yaml(yaml_file)
    yaml_content["master-server"]["aws"]["ports"] = new_ports
    write_yaml(yaml_content, yaml_file)

def set_domain_internal_domain(value, yaml_file):
    """
    targets builder/projects/elife.yaml
    """
    print "setting domain name " + value
    yaml_content = get_yaml(yaml_file)
    internal = value.split(".")[0] + ".internal"
    yaml_content["defaults"]["domain"] = value
    yaml_content["defaults"]["intdomain"] = internal
    write_yaml(yaml_content, yaml_file)

def set_private_builder_repo(value, yaml_file):
    """
    targets builder/projects/elife.yaml
    """
    new_value = "ssh://git@github.com/" + value
    print "setting builder private repo " + new_value
    yaml_content = get_yaml(yaml_file)
    yaml_content["defaults"]["private-repo"] = new_value
    write_yaml(yaml_content, yaml_file)

def set_drupal_endpoint():
    # drupal_EIF_endpoint = 'http://52.2.70.162/api/article.json'
    # drupal_approve_endpoint = 'http://52.2.70.162/api/publish/'
    # TODO: complete this function
    pass

def set_lax_deploy_user_email(value, yaml_file):
    """
    needs to target builder-private/pillar/elife.sls
    is needed to prevent failure of lett's encrypt configuration
    """
    # TODO: complete this function
    pass

def set_website_passwords(passwords, yaml_file):
    yaml_content = get_yaml(yaml_file)
    yaml_content["elife_website"]["db"]["password"] = passwords[0]
    yaml_content["elife_website"]["db_test"]["password"] = passwords[1]
    yaml_content["elife_website"]["drupal_user"]["password"] = passwords[2]
    write_yaml(yaml_content, yaml_file)

def set_lax_app_credentials(passwords, yaml_file):
    yaml_content = get_yaml(yaml_file)
    yaml_content["lax"]["app"]["secret"] = passwords[0]
    yaml_content["lax"]["db"]["username"] = passwords[1]
    yaml_content["lax"]["db"]["password"] = passwords[2]
    write_yaml(yaml_content, yaml_file)

def gen_website_base_url(domain, prefix, instance_name, yaml_file):
    # TODO: complete this function
    yaml_content = get_yaml(yaml_file)
    subdomain = yaml_content["elife-website"]["subdomain"]
    website_base_url = subdomain + instance_name + "-" + "website" + "-" + "prefix" + domain
    return website_base_url

def set_dashboard_specific_config(domain, prefix, instance_name, queues, py_setting, yaml_file):
    """
    The dashboard settings file needs to have:

    http auth
    sqs_region
    rds_region
    preview_base_url - can be inferred from other config!
    event_monitor_queue
    workflow_starter_queue
    the scheduler is available on localhost as it is deployed to the same machine!
    there are no explicit secrets in this file!

    of these
    http auth
    sqs_region
    rds_region
    have already been set in this script. preview base url can be derviced from the prefix.
    """
    website_base_url = gen_website_base_url(domain, prefix, instance_name, yaml_file)
    event_monitor_queue = prefix + "-" + queues["event_monitor_queue"]
    workflow_starter_queue = prefix + "-" + queues["workflow_starter_queue"]
    set_base_url_in_python_settings(website_base_url, py_setting)
    set_event_queue_in_python_settings(event_monitor_queue, py_setting)
    set_workflow_queue_in_python_settings(workflow_starter_queue, py_setting)

def set_bot_aws_resources(preifx, buckets, queues, py_setting):
    line_identifiers = ["publishing_buckets_prefix"]
    set_element_in_python_settings(prefix, line_identifiers, py_setting)

    for key in buckets.keys():
        line_identifiers = [key]
        set_element_in_python_settings(buckets[key], line_identifiers, py_setting)

    for key in queues.keys():
        line_identifiers = [key]
        value = prefix + "-" + queues[key]
        print value
        set_element_in_python_settings(value, line_identifiers, py_setting)

def set_deploy_user_email(value, yaml_file):
    yaml_content = get_yaml(yaml_file)
    yaml_content["elife"]["deploy_user"]["email"] = deploy_email
    write_yaml(yaml_content, yaml_file)

def set_scheduler_config(user, password, py_setting):
    line_identifiers = ["PUBLISHING_SERVICE_USER"]
    set_element_in_python_settings(user, line_identifiers, py_setting)
    line_identifiers = ["PUBLISHING_SERVICE_PASSWORD"]
    set_element_in_python_settings(password, line_identifiers, py_setting)

def set_dashboard_secrets(aws_credentials, http_auth, scheduler, yaml_file):
    yaml_content = get_yaml(yaml_file)
    yaml_content["elife_dashboard"]["aws"]["username"] = aws_credentials[0]
    yaml_content["elife_dashboard"]["aws"]["access_id"] = aws_credentials[1]
    yaml_content["elife_dashboard"]["aws"]["secret_access_key"] = aws_credentials[2]
    yaml_content["elife_dashboard"]["basic_auth"]["username"] = http_auth[0]
    yaml_content["elife_dashboard"]["basic_auth"]["password"] = http_auth[1]
    yaml_content["elife_article_scheduler"]["secret_key"] = scheduler[0]
    yaml_content["elife_article_scheduler"]["db"]["username"] = scheduler[1]
    yaml_content["elife_article_scheduler"]["db"]["password"] = scheduler[2]
    write_yaml(yaml_content, yaml_file)

def set_bot_aws_credentials(credentials, py_setting):
    aws_user = credentials[0]
    aws_key = credentials[1]
    aws_secret = credentials[2]
    line_identifiers = ["aws_access_key_id"]
    set_element_in_python_settings(aws_key, line_identifiers, py_setting)
    line_identifiers = ["aws_secret_access_key"]
    set_element_in_python_settings(aws_secret, line_identifiers, py_setting)


if __name__ == "__main__":
    # TODO: remember to ask if we can change the description in
    # /Users/ian/workbench/builder-private-test/pillar/elife.sls for the default user.

    # TODO: set poa_bucket and other downstream options

    # TODO: either put LENS CDN, and other info, into continuum.yaml or derive them directly from AWS progromatically.

    # we assume that instance name is going to be the same
    # for different services.
    # instance_name = raw_input("what is your instance name? ")
    instance_name = "test"

    full_config, full_private_config = set_config_paths(CONFIG, PRIVATE_CONFIG, builder_path, builder_private_path)
    check_config_files_existence(full_config)
    check_config_files_existence(full_private_config)

    bot_py = full_private_config["bot"]
    dashboard_py = full_private_config["dashboard"]
    scheduler_py = full_private_config["scheduler"]

    elife_global_yaml = full_config["elife"]
    elife_private_yaml = full_private_config["elife"]
    lax_private_yaml = full_private_config["lax"]
    website_private_yaml = full_private_config["website"]
    dashboard_private_yaml = full_private_config["dashboard_yaml"]

    # aws global settings
    set_aws_region(region, elife_global_yaml, python_settings=[bot_py, dashboard_py])

    # set aws settings across config files
    set_dashboard_aws_credentials(bot_aws_user, bot_aws_key, bot_aws_secret, dashboard_private_yaml)

    #set lax API credentials
    set_dashboard_basic_auth(dashboard_user, dashboard_password, dashboard_private_yaml)
    set_lax_basic_auth(crazy_user, crazy_password, elife_private_yaml, bot_py) # sets bot py with crazy password for lax.
    set_web_basic_auth(web_user, web_password, elife_private_yaml)

    # bilder global settings
    set_domain_internal_domain(domain_name, elife_global_yaml)
    set_private_builder_repo(builder_private_repo, elife_global_yaml)
    # # the following all affect buider/projects/elife.yaml
    # # ideally we should be able to find out these details via the AWS API
    set_vpc_id(VPC_ID, elife_global_yaml)
    set_subnet_id(SUBNET_ID_A, elife_global_yaml)
    set_subnet_cidr(SUBNET_CIDR, elife_global_yaml)
    set_rds_subnets(RDS_SUBNETS, elife_global_yaml)
    set_cidr_ip(SUBNET_CIDR, elife_global_yaml)
    set_ami(MACHINE_AMI, elife_global_yaml)

    # set email for let's encrypt
    set_deploy_user_email(deploy_email, elife_private_yaml)
    # TODO: check whether region needs to be set for deploy user, along with
    # the AWS creds in this file!

    ## turn off write keyparis
    # TODO: turn_off_write_keyparis

    ## point bot to lax server
    lax_update, lax_versions = derive_lax_endpoint_from_domain(domain_name, instance_name)
    set_lax_update(lax_update, bot_py)
    set_lax_versions(lax_versions, bot_py)

    ## set lax secret credentials
    lax_creds = [lax_app_secret, lax_db_username, lax_db_password]
    set_lax_app_credentials(lax_creds, lax_private_yaml)

    ## Drupal/elife-website config
    elife_website_passwords = [drupal_db_password, drupal_db_test_password, drupal_user_password]
    set_website_passwords(elife_website_passwords, website_private_yaml)

    ## Set bot queues and prefix
    # NOTE: this will need to be altered when J Root changes the handling of queue settings for the bot, as discussed 2016-08-02
    set_bot_aws_resources(prefix, s3_buckets, queue_map, bot_py)
    aws_creds = [bot_aws_user, bot_aws_key, bot_aws_secret]
    set_bot_aws_credentials(aws_creds, bot_py)

    ## additional dashboard settings
    set_dashboard_specific_config(domain_name, prefix, instance_name, queue_map, dashboard_py, elife_global_yaml)

    ## Scheduler
    # sets /salt/elife-dashboard/config/srv-elife-article-scheduler-default_settings.py
    # the PUBLISHING_SERVICE_PASSWORD is the same as the password set in pillar/elife.sls for basic auth!
    # DASHBOARD_PUBLISHING_SERVICE - is on localhost, does not need to be set
    # PUBLISHING_SERVICE_USER
    # PUBLISHING_SERVICE_PASSWORD
    set_scheduler_config(dashboard_user, dashboard_password, scheduler_py)

    ## private pillar/elife-dashboard.sls
    # dasbhard_db_username
    # dashboard_db_password
    # basic_auth_username
    # basic_auth_password  - same as other basic auth config
    # elife_article_scheduler app secret_key
    # elife_article_scheduler secret_key
    # scheduler db password
    http_auth = [dashboard_user, dashboard_password]
    scheduler_details = [scheduler_app_secret, scheduler_db_username, scheduler_db_password]
    set_dashboard_secrets(aws_creds, http_auth, scheduler_details, dashboard_private_yaml)

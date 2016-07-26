import sys
import os
import boto3
import ruamel.yaml # ruamel preserves yaml order and comments
from ruamel.yaml import dump as MyDump
from aws_setting_utils import s3_buckets, prefix, region, queue_map, builder_path, builder_private_path
from aws_setting_utils import http_user, http_password, crazy_user, crazy_password, web_user, web_password
from aws_setting_utils import bot_aws_user, bot_aws_key, bot_aws_secret, domain_name
from aws_setting_utils import dashboard_aws_user, dashboard_aws_key, dashboard_aws_secret
from aws_setting_utils import builder_private_repo

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
RDS_SUBNETS = [SUBNET_ID_A, SUBNET_ID_B]

CONFIG = {"elife":"projects/elife.yaml"}

PRIVATE_CONFIG = {
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
    print "writing " + path
    yaml_content = ruamel.yaml.dump(yaml_content, Dumper=ruamel.yaml.RoundTripDumper, indent=4)
    new_yaml = yaml_content.replace(" -", "     -")
    new_yaml_two = new_yaml.replace("-   ", "- ")
    target = open(path,"w")
    target.write(new_yaml_two)
    target.close()
    # TODO: this is writing content back incorrectly, need to look at bit harder at this.
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
                line = "".join(line.split("=")[:-1]) + " = " + value + "\n"
                # print line
        new_file.append(line)
    new_file_content = "".join(new_file)
    # target = open(settings_file,"w").write(new_file_content)
    # target.close()

def set_region_in_python_settings(value, settings_file):
    """
    targets settings.py in elife-bot
    """
    print "setting " + value + " in " + settings_file
    line_identifiers = ["simpledb_region","ses_region","sqs_region"]
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
    elife_yaml_content["elife"]["web_users"][""]["username"] = http_user
    elife_yaml_content["elife"]["web_users"][""]["password"] = http_password
    write_yaml(elife_yaml_content, elife_yaml)

def set_lax_basic_auth(http_user, http_password, elife_yaml, bot_py):
    elife_yaml_content = get_yaml(elife_private_yaml)
    elife_yaml_content["elife"]["web_users"]["crazy-"]["username"] = http_user
    elife_yaml_content["elife"]["web_users"]["crazy-"]["password"] = http_password
    write_yaml(elife_yaml_content, elife_yaml)
    line_identifiers = ["lax_update_user"]
    value = http_user
    set_element_in_python_settings(value, line_identifiers, bot_py)
    line_identifiers = ["lax_update_pass"]
    value = http_password
    set_element_in_python_settings(value, line_identifiers, bot_py)

def set_dashboard_aws_credentials(user, key, secret, dashboard_private_yaml):
    dashboard_yaml_content = get_yaml(dashboard_private_yaml)
    dashboard_yaml_content["elife_dashboard"]["aws"]["username"] = user
    dashboard_yaml_content["elife_dashboard"]["aws"]["access_id"] = key
    dashboard_yaml_content["elife_dashboard"]["aws"]["secret_access_key"] = secret
    write_yaml(dashboard_yaml_content, dashboard_private_yaml)

def set_lax_update(lax_endpoint, bot_py):
    value = lax_endpoint
    line_identifiers = ["lax_article_versions"]
    set_element_in_python_settings(lax_endpoint, line_identifiers, bot_py)

def set_lax_versions(lax_endpoint, bot_py):
    value = lax_endpoint
    line_identifiers = ["lax_update"]
    set_element_in_python_settings(lax_endpoint, line_identifiers, bot_py)

def derive_lax_endpoint_from_domain(domain):
    # instance_name = raw_input("what is your lax instance name? ")
    instance_name = "test"
    lax_server = instance_name + "--lax." + domain
    lax_update = lax_server + "/api/v1/article/create-update/"
    lax_article_versions = lax_server + "api/v1/article/10.7554/eLife.{article_id}/version/"
    print "lax update endpoint: " + lax_update
    print "lax article versions endpoint: " + lax_article_versions
    return lax_update, lax_article_versions

def set_vpc_id(vpc_id, elife_global_yaml):
    elife_global_yaml_content = get_yaml(elife_global_yaml)
    elife_global_yaml_content["defaults"]["aws"]["vpc-id"] = vpc_id
    write_yaml(elife_global_yaml_content, elife_global_yaml)

def set_subnet_id(subnet_id, elife_global_yaml):
    elife_global_yaml_content = get_yaml(elife_global_yaml)
    elife_global_yaml_content["defaults"]["aws"]["subnet-id"] = subnet_id
    write_yaml(elife_global_yaml_content, elife_global_yaml)

def set_subnet_cidr(subnet_cidr, elife_global_yaml):
    elife_global_yaml_content = get_yaml(elife_global_yaml)
    elife_global_yaml_content["defaults"]["aws"]["subnet-cidr"] = subnet_cidr
    write_yaml(elife_global_yaml_content, elife_global_yaml)

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
    targets builder/projects/elife.yaml
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

if __name__ == "__main__":
    full_config, full_private_config = set_config_paths(CONFIG, PRIVATE_CONFIG, builder_path, builder_private_path)
    check_config_files_existence(full_config)
    check_config_files_existence(full_private_config)

    elife_global_yaml = full_config["elife"]
    elife_private_yaml = full_private_config["elife"]
    dashboard_private_yaml = full_private_config["dashboard_private"]
    bot_py = full_private_config["bot"]
    dashboard_py = full_private_config["dashboard"]
    scheduler_py = full_private_config["scheduler"]

    # aws global settings
    set_aws_region(region, elife_global_yaml, python_settings=[bot_py, dashboard_py, scheduler_py])

    #set lax API credentials
    set_dashboard_basic_auth(http_user, http_password, dashboard_private_yaml)
    set_lax_basic_auth(crazy_user, crazy_password, elife_private_yaml, bot_py)
    set_web_basic_auth(web_user, web_password, elife_private_yaml) # TODO: check if the implied wildchard in the elife.sls file causes this parser to output a `?`, and whether that is going to cause a problem.

    set_dashboard_aws_credentials(dashboard_aws_user, dashboard_aws_key, dashboard_aws_secret, dashboard_private_yaml)

    set_domain_internal_domain(domain_name, elife_global_yaml)
    #
    set_private_builder_repo(builder_private_repo, elife_global_yaml)

    # # the following all affect buider/projects/elife.yaml
    # # ideally we should be able to find out these details via the AWS API
    set_vpc_id(VPC_ID, elife_global_yaml)
    set_subnet_id(SUBNET_ID_A, elife_global_yaml)
    set_subnet_cidr(SUBNET_CIDR, elife_global_yaml)
    set_rds_subnets(RDS_SUBNETS, elife_global_yaml)
    set_cidr_ip(SUBNET_CIDR, elife_global_yaml)

    # # set email for let's encrypt

    # # turn off write keyparis
    #turn_off_write_keyparis

    # # point bot to lax server
    # TODO: set this config part to be live
    lax_update, lax_versions = derive_lax_endpoint_from_domain(domain_name)
    set_lax_update(lax_update, bot_py)
    set_lax_versions(lax_versions, bot_py)

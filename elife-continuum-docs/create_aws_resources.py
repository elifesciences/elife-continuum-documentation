import boto3
from botocore.client import Config
from aws_setting_utils import s3_buckets, prefix, region, queue_map

# v4 authenticatio is being rolled out across all of AWS, so we need to update
# the creat script 
s3 = boto3.resource('s3', region_name=region, config=Config(signature_version='s3v4'))
sqs = boto3.client('sqs', region_name=region)
swf = boto3.client('swf', region_name=region)

s3_buckets_names = s3_buckets.values()

# we need the full queue dict as we need to be able to identify
# which queue is associated with the `website_ingest_queue` label.
# This is the queue that needs to have a policy associated with the
# incoming AWS s3 bucket.
sqs_queues = queue_map.values()


def generate_bucket_arn_from_name(bucket_name):
    """
    the bucket arn that we require for setting a policy on an SQS queue can be
    derived directly from the bucket name, meaning we do not need to make
    any calls to AWS to obtain this if we already have the bucket name.

    >>> generate_bucket_arn_from_name(name)
    arn:aws:s3:*:*:name
    """
    return "arn:aws:s3:*:*:" + bucket_name

def get_event_monitor_queue_name(prefix):
    try:
        queue_name = queue_map["website_ingest_queue"]
        return prefix + "-" + queue_name
    except:
        raise error

def get_production_final_bucket(prefix):
    try:
        bucket_name = s3_buckets["production_bucket"]
        return prefix + "-" + bucket_name
    except:
        raise error

def get_sqs_arn_for_incoming_queue(prefix):
    """
    we need to set a policy on the incoming bucket to allow it to trigger events into
    an approprirate sqs queue. To do that we need to identify the queue arn for that queue.
    This depends on the existence of the queue with the key `event_monitor_queue`.
    """
    incoming_queue_name = get_event_monitor_queue_name(prefix)
    queues = sqs.list_queues()
    queue_urls = queues["QueueUrls"]
    for queue in queue_urls:
        queue_simple_name = queue.split("/")[-1]
        if queue_simple_name == incoming_queue_name: # if the incoming queue exists, then get it's ARN
            queue_attributes = sqs.get_queue_attributes(QueueUrl=queue, AttributeNames=["QueueArn", "Policy"])
            queue_arn = queue_attributes["Attributes"]["QueueArn"]
            queue_url = queue
    return queue_arn, queue_url

# Bucket Creation
def create_bucket(s3, bucket, region):
    print "creating bucket: " + bucket + " in region " + region
    if region == "us-east-1": # AWS api is inconsistent
        s3.create_bucket(Bucket=bucket)
    else:
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': region})
    return True

def create_prefixed_buckets(s3, prefix, region):
    for bucket in s3_buckets_names:
        create_bucket(s3, prefix + "-" + bucket, region)

# SQS creation
def create_prefixed_queues(prefix):
    """
    create a set of queues based on a map set in continuum.yaml
    """
    for queue in sqs_queues:
        queue_name = prefix + "-" + queue
        print "creating queue: " + queue_name
        result = sqs.create_queue(QueueName=queue_name)

# SWF Creation
def create_prefixed_swf_domain(prefix):
    registered_domains = swf.list_domains(registrationStatus='REGISTERED')
    reg_domain_info = registered_domains["domainInfos"]
    reg_domain_count = len(reg_domain_info)

    deprecated_domains = swf.list_domains(registrationStatus='DEPRECATED')
    dep_domain_info = deprecated_domains["domainInfos"]
    dep_domain_count = len(dep_domain_info)

    print "you currently have " + str(reg_domain_count) + " regiesterd domains"
    depricated_domains = swf.list_domains(registrationStatus='DEPRECATED')
    print "you currently have " + str(dep_domain_count) + " deprecated domains"
    print "you have " + str(100 - dep_domain_count - reg_domain_count) + " domains left"

    #
    # if the domain is already registered, don't do anything
    # if the domain is depricated, report back
    # otherwise, create the domain
    #
    create_domain = True
    swf_name = "Publish." + prefix
    for domain in reg_domain_info:
        if swf_name == domain["name"]:
            print "domain is already registered !"
            create_domain = False
    for domain in dep_domain_info:
        if swf_name == domain["name"]:
            print "domain is depricated, cannot register, you will need to pick another domain name"
            create_domain = False
    if create_domain:
        print "creating swf domain: " + swf_name
        swf.register_domain(name=swf_name, description="test SWF domain for thie postfixed namespace", workflowExecutionRetentionPeriodInDays="90")

# Policy generation
def generate_sqs_policy(sqs_arn, bucket_arn):
    policy_doc_template = open("continuum_aws_policy_tempaltes/sqs_policy_template.json", "r").read()
    policy_doc =  policy_doc_template % (sqs_arn, sqs_arn, bucket_arn)
    return policy_doc

def set_policy_on_queue(prefix):
    event_monitor_queue = get_event_monitor_queue_name(prefix)
    production_bucket = get_production_final_bucket(prefix)
    monitor_bucket_arn = generate_bucket_arn_from_name(production_bucket)
    event_queue_arn, queue_url = get_sqs_arn_for_incoming_queue(prefix)
    policy = generate_sqs_policy(event_queue_arn, monitor_bucket_arn)
    response = sqs.set_queue_attributes(QueueUrl=queue_url, Attributes={"Policy":policy})
    print response

def set_notification_on_bucket(prefix):
    production_bucket = get_production_final_bucket(prefix)
    notification = s3.BucketNotification(production_bucket)
    event_queue_arn, queue_url = get_sqs_arn_for_incoming_queue(prefix)
    data = {}
    data['QueueConfigurations'] = [
                {
                    'QueueArn': event_queue_arn,
                    'Events': ["s3:ObjectCreated:*"]
                    }
                ]
    response = notification.put(NotificationConfiguration=data)
    print response

def generate_cdn_arn_from_name(bucket_name):
    """
    the bucket arn that we require for setting a policy on an SQS queue can be
    derived directly from the bucket name, meaning we do not need to make
    any calls to AWS to obtain this if we already have the bucket name.

    >>> generate_bucket_arn_from_name(name)
    arn:aws:s3:*:*:name
    """
    return "arn:aws:s3:::" + bucket_name

def get_cdn_bucket(prefix):
    try:
        bucket_name = s3_buckets["ppp_cdn_bucket"]
        return prefix + "-" + bucket_name
    except:
        raise error

def generate_cdn_policy(arn):
    cdn_arn = arn + "/*" # trailling backslash star needed to correctly configure permission on CDN content
    policy_doc_template = open("continuum_aws_policy_tempaltes/cdn_permission_template.json").read()
    policy_doc =  policy_doc_template % (cdn_arn)
    return policy_doc

def set_policy_on_cdn(prefix):
    cdn_bucket = get_cdn_bucket(prefix)
    bucket_policy = s3.BucketPolicy(cdn_bucket)
    cdn_arn = generate_cdn_arn_from_name(cdn_bucket)
    cdn_policy = generate_cdn_policy(cdn_arn)
    response = bucket_policy.put(Policy=cdn_policy)
    print response

if __name__ == "__main__":
    create_prefixed_queues(prefix)
    create_prefixed_buckets(s3, prefix, region)
    create_prefixed_swf_domain(prefix)
    set_policy_on_queue(prefix)
    set_notification_on_bucket(prefix)
    set_policy_on_cdn(prefix)

    ## policy settings
    # configure the CDN permissions s3_buckets["ppp_cdn_bucket"] (with the prefix)

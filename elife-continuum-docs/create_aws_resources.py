import boto3
from aws_setting_utils import s3_buckets, prefix, region, queue_map

s3 = boto3.resource('s3', region_name=region)
sqs = boto3.client('sqs', region_name=region)
swf = boto3.client('swf', region_name=region)

s3_buckets = s3_buckets.values()

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
        print prefix + "-" + queue_name
        return prefix + "-" + queue_name
    except:
        raise error

def get_sqs_arn_for_incoming_queue(prefix):
    """
    we need to set a policy on the incoming bucket to allow it to trigger events into
    an approprirate sqs queue. To do that we need to identify the queue arn for that queue.
    This depends on the existence of the queue with the key `event_monitor_queue`.
    """
    incoming_queue_name = get_event_monitor_queue_name(prefix)
    queues = sqs.list_queues()["QueueUrls"]
    for queue in queues:
        queue_simple_name = queue.split("/")[-1]
        if queue_simple_name == incoming_queue_name: # if the incoming queue exists, then get it's ARN
            queue_attributes = sqs.get_queue_attributes(QueueUrl=queue, AttributeNames=["QueueArn", "Policy"])
            queue_arn = queue_attributes["Attributes"]["QueueArn"]
    return queue_arn

# Bucket Creation
def create_bucket(s3, bucket, region):
    print "creating bucket: " + bucket
    if region == "us-east-1": # AWS api is inconsistent
        s3.create_bucket(Bucket=bucket)
    else:
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': region})
    return True

def create_prefixed_buckets(s3, prefix, region):
    for bucket in s3_buckets:
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
    policy_doc_template = open("continuum_aws_policy_tempaltes/sqs_policy_template.json", "r").readlines()
    policy_doc =  policy_doc_template % (sqs_arn,sqs_arn, bucket_arn)
    return policy_doc

if __name__ == "__main__":
    get_event_monitor_queue_name(prefix)
    create_prefixed_queues(prefix)
    create_prefixed_buckets(s3, prefix, region)
    create_prefixed_swf_domain(prefix)

    ## policy settings
    # configure the bucket permissions for the s3_buckets["production_bucket"] (with the prefix)
    # configure the queue permissions for the sqs_queues["S3_monitor_queue"] (with the prefix)
    # configure the CDN permissions s3_buckets["ppp_cdn_bucket"] (with the prefix)

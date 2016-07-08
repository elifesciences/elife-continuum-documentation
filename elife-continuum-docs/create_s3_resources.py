import boto3
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("-p", "--prefix", dest="prefix", help="provide a bucket name prefix")
parser.add_argument("-d", "--delete", action="store_true", default=False , dest="delete", help="delete buckets")

location = "us-east-1"
allowed_deletion_prefixes = ["ct","pppim"]

# S3 info derioved from bot settings,
# https://github.com/elifesciences/builder/blob/master/salt/salt/elife-bot/config/opt-elife-bot-settings.py#L25-L27

required_buckets = {"production_bucket" : 'elife-production-final',
                    "eif_bucket" : 'elife-publishing-eif',
                    "expanded_bucket" : 'elife-publishing-expanded',
                    "ppp_cdn_bucket" : 'elife-publishing-cdn',
                    "archive_bucket" : 'elife-publishing-archive',
                    "xml_bucket" : 'elife-publishing-xml'}

# queue info derioved from dashboard settings, and bot settings,
# e.g. https://github.com/elifesciences/builder/blob/master/salt/salt/elife-dashboard/config/srv-app-dashboard-prod_settings.py#L9-L11
# https://github.com/elifesciences/builder/blob/master/salt/salt/elife-bot/config/opt-elife-bot-settings.py#L25-L27
required_queues = {"S3_monitor_queue" : 'incoming-queue',
                    "event_monitor_queue" : 'event-property-incoming-queue',
                    "workflow_starter_queue" : 'workflow-starter-queue'}

def delete_bucket(bucket):
    for key in bucket.objects.all():
        key.delete()
    bucket.delete()
    return True

def set_notification_on_bucket(bucket_name):
    bucket_notification = s3.BucketNotification('bucket_name')

def create_bucket(s3, bucket_name, location):
    print bucket_name, location
    if location == "us-east-1":
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': location})
    return True

def get_prefixed_buckets(s3, prefix):
    prefixed_buckets = []
    for bucket in s3.buckets.all():
        bucket_name = bucket.name
        if bucket_name.find(prefix + "-") > -1:
            prefixed_buckets.append(bucket)
    return prefixed_buckets

def delete_prefixed_buckets(prefix):
    if prefix not in allowed_deletion_prefixes:
        raise ValueError("you are not allowed to delete that bucket")
    prefixed_buckets = get_prefixed_buckets(prefix)
    print "I may try to delete these buckets ", prefixed_buckets
    for bucket in prefixed_buckets: delete_bucket(bucket)
    return True

def create_prefixed_buckets(s3, prefix):
    for bucket in required_buckets.values():
        create_bucket(s3, prefix + "-" + bucket, location)

def create_prefixed_queues(prefix):
    for queue in required_queues.values():
        sqs.create_queue(QueueName=prefix + "-" + queue)

def create_prefixed_swf_domain(prefix):
    swf.register_domain(name="Publish" + "." + prefix, description="test SWF domain for thie postfixed namespace", workflowExecutionRetentionPeriodInDays="90")

def create_bot_aws_resources(prefix):
    # create_prefixed_queues(prefix)
    create_prefixed_swf_domain(prefix)
    # create_prefixed_buckets(prefix)

def set_bucket_notification():
    bucket_notification = s3.BucketNotification('bucket_name')
    bucket_notification.put(QueueConfigurations[QueueArn:])

def set_queue_notification(queue_arn):
    bucket_notification = s3.BucketNotification('ct-elife-production-final')
    print bucket_notification.__dict__
    data = {}
    # for valid event types see  http://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html#supported-notification-event-types
    data['QueueConfigurations'] = [
                {
                    'QueueArn': queue_arn,
                    'Events': ["s3:ObjectCreated:*"]
                    }
                ]

    response = bucket_notification.put(NotificationConfiguration=data)
    print response

def get_queue_arn(prefix):
    queues = sqs.list_queues()["QueueUrls"]
    for queue in queues:
        queue_simple_name = queue.split("/")[-1]
        if queue_simple_name == prefix + "-incoming-queue":
            queue_attributes = sqs.get_queue_attributes(QueueUrl=queue, AttributeNames=["QueueArn", "Policy"])
            queue_arn = queue_attributes["Attributes"]["QueueArn"]
    return queue_arn

def generate_bucket_arn_from_name(bucket_name):
    """
    the bucket arn that we require for setting a policy on an SQS queue can be
    derived directly from the bucket name, meaning we do not need to make
    any calls to AWS to obtain this if we already have the bucket name.

    >>> generate_bucket_arn_from_name(name)
    arn:aws:s3:*:*:name
    """
    return "arn:aws:s3:*:*:" + bucket_name

def generate_sqs_policy(sqs_arn, bucket_arn):
    policy_doc =  """  {
        "Version": "2012-10-17",
        "Id": "%s/SQSDefaultPolicy",
        "Statement": [
          {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
              "AWS": "*"
            },
            "Action": "SQS:SendMessage",
            "Resource": "%s",
            "Condition": {
              "ArnLike": {
                "aws:SourceArn": "%s"
              }
            }
          }
        ]
      }
      """ % (sqs_arn,sqs_arn, bucket_arn)
    return policy_doc

def generate_sqs_policy_json(sqs_arn, bucket_arn):
    policy_doc = {  "Version": "2012-10-17",
                    "Id": sqs_arn+"/SQSDefaultPolicy",
                    "Statement": [
                          {
                            "Sid": "",
                            "Effect": "Allow",
                            "Principal": {
                              "AWS": "*"
                            },
                            "Action": "SQS:SendMessage",
                            "Resource": sqs_arn,
                            "Condition": {
                                "ArnLike": {
                                "aws:SourceArn": bucket_arn
                                }
                            }
                        }
                    ]
                }
    return policy_doc

def set_queue_policy(prefix):
    queues = sqs.list_queues()["QueueUrls"]
    for queue in queues:
        queue_simple_name = queue.split("/")[-1]
        if queue_simple_name == prefix + "-incoming-queue":
            bucket_arn = generate_bucket_arn_from_name("ct-elife-production-final")
            sqs_arn = get_queue_arn(prefix)
            policy = generate_sqs_policy(sqs_arn, bucket_arn)
            response = sqs.set_queue_attributes(QueueUrl=queue, Attributes={"Policy":policy})
            print response

if __name__ == "__main__":
    # TODO: figure out the difference between boto3.resource and boto3.client for this code
    s3 = boto3.resource('s3')
    sqs = boto3.client('sqs')
    swf = boto3.client('swf')

    args = parser.parse_args()
    prefix = args.prefix
    delete = args.delete

    if delete:
        print "about to try to delete some buckets"
        delete_prefixed_buckets(prefix)
    else:
        aws_arn = generate_bucket_arn_from_name("ct-elife-production-final")
        sqs_arn = get_queue_arn(prefix)
        policy = generate_sqs_policy(sqs_arn, aws_arn)
        print policy
        policy_json = generate_sqs_policy_json(sqs_arn, aws_arn)
        print policy_json
        # set_queue_policy(prefix)
        # bucket_arn = get_bucket_arn(prefix)
        queue_arn = get_queue_arn(prefix)
        set_queue_notification(queue_arn)

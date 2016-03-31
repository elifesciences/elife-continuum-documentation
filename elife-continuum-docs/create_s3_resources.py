import boto3
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("-p", "--prefix", dest="prefix", help="provide a bucket name prefix")
parser.add_argument("-d", "--delete", action="store_true", default=False , dest="delete", help="delete buckets")

location = "us-east-1"
allowed_deletion_prefixes = ["ct","pppim"]
required_buckets = {"production_bucket" : 'elife-production-final',
                    "eif_bucket" : 'elife-publishing-eif',
                    "expanded_bucket" : 'elife-publishing-expanded',
                    "ppp_cdn_bucket" : 'elife-publishing-cdn',
                    "archive_bucket" : 'elife-publishing-archive',
                    "xml_bucket" : 'elife-publishing-xml'}

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

def create_bucket(bucket_name, location):
    print bucket_name, location
    if location == "us-east-1":
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': location})
    return True

def get_prefixed_buckets(prefix):
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

def create_prefixed_buckets(prefix):
    for bucket in required_buckets.values():
        create_bucket(prefix + "-" + bucket, location)

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

def set_queue_notification():
    ???

if __name__ == "__main__":
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
        print "about to try to create some buckets"
        create_bot_aws_resources(prefix)

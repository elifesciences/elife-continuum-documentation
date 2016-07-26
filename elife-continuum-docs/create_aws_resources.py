import boto3
from aws_setting_utils import s3_buckets, prefix, region, queue_map
s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')
swf = boto3.client('swf')

print queue_map
s3_buckets_names = s3_buckets.values()


# generic functions
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
    for bucket in s3_bucket:
        create_bucket(s3, prefix + "-" + bucket, region)

# SQS creation
def create_prefixed_queues(prefix):
    for queue in sqs_queues:
        queue_name = prefix + "-" + queue
        print "creating queue: " + queue_name
        sqs.create_queue(QueueName=queue_name)

# SWF Creation
def create_prefixed_swf_domain(prefix):
    swf_name = "Publish." + prefix
    print "creating swf domain: " + swf_name
    swf.register_domain(name=swf_name, description="test SWF domain for thie postfixed namespace", workflowExecutionRetentionPeriodInDays="90")

if __name__ == "__main__":
    # Do resource creation
    get_event_monitor_queue_name(prefix)
    # create_prefixed_queues(prefix)
    # create_prefixed_swf_domain(prefix)
    # create_prefixed_buckets(prefix)



# def set_notification_on_bucket(bucket_name):
#     bucket_notification = s3.BucketNotification('bucket_name')
#
#
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

#
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

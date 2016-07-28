import sys
from aws_setting_utils import prefix, region
from aws_setting_utils import s3_protected_queues,  s3_protected_buckets, protected_prefixes
import boto3

s3 = boto3.resource('s3', region_name=region)
sqs = boto3.client('sqs', region_name=region)
swf = boto3.client('swf', region_name=region)

def check_prefix_against_protected(pre, protected):
    if pre in protected:
        return True
    if pre not in protected:
        return False
    else:
        sys.exit()

def check_candidates_against_protected(candidates, protected):
    """
    use sets to check whether there is any common membership
    """
    if bool(set(candidates) & set(protected)):
        return True
    else:
        return False

def check_buckets_against_protected(buckets, protected_buckets):
    if check_candidates_against_protected(buckets, protected_buckets):
        print "warning, a protected buckets has been found, am about to exit"
        sys.exit()
    else:
        pass

def check_queues_against_protected(queues, s3_protected_queues):
    if check_candidates_against_protected(queues, s3_protected_queues):
        print "warning, a protected queue has been found, am about to exit"
        sys.exit()
    else:
        pass

def confirm_deletion(resources):
    print resources
    check_resource = resources[-1] # get the user to type this in as a sanity check
    print "WARNING, you are about to delete the following resources: "
    for r in resources:
        print "\t " + r
    response = raw_input("in order to delete these resources please type: " + check_resource + "\n > ")
    if response == check_resource:
        print "about to delte all the things!!"
    else:
        print "oops, that's didn't match, I'm going to abort now"
        sys.exit()

def delete_bucket(bucket):
    """
    to delete an S3 bucket we have to itertate through and delete all of the keys
    within the bucket.
    """
    for key in bucket.objects.all():
        key.delete()
    bucket.delete()
    return True

def get_prefixed_buckets(prefix):
    prefixed_buckets = []
    bucket_names = []
    for bucket in s3.buckets.all():
        bucket_name = bucket.name
        if bucket_name.find(prefix + "-") > -1:
            prefixed_buckets.append(bucket)
            bucket_names.append(bucket_name)
    return prefixed_buckets, bucket_names

def delete_prefixed_buckets(prefix):
    print "about to attempt to delete buckets ..."
    buckets, bucket_names = get_prefixed_buckets(prefix)
    if buckets:
        check_buckets_against_protected(buckets, s3_protected_buckets)
        confirm_deletion(bucket_names)
        for n, bucket in enumerate(buckets):
            print "deleting: " + bucket_names[n]
            delete_bucket(bucket)
    else:
        print "nothing found to delete"

def get_prefixed_queues(prefix):
    prefixed_queues = []
    prefixed_queue_urls = []
    list_queues = sqs.list_queues()
    if "QueueUrls" in list_queues:
        for queue in sqs.list_queues()["QueueUrls"]:
            print queue
            queue_name = queue.split("/")[-1]
            if queue_name.find(prefix + "-") > -1:
                prefixed_queue_urls.append(queue)
                prefixed_queues.append(queue_name)
    else:
        print "no queus found for deletion"
    return prefixed_queue_urls, prefixed_queues


def delete_prefixed_queues(prefix):
    print "about to attempt to delete queues ..."
    queue_urls, queues = get_prefixed_queues(prefix)
    if queues:
        check_queues_against_protected(queues, s3_protected_queues)
        confirm_deletion(queues)
        for queue in queue_urls:
            print "deleteing: " + queue
            sqs.delete_queue(QueueUrl=queue)
    else:
        print "nothing found to delete"

def delete_domain(prefix):
    # TODO: looks like I can only depricate a domain, but then the domain seems to be hanging around
    # so a second deleetion attempt fails.
    print """ Currently Domains cannot be deleted, do not detele or depricate domains, please
    just re-use domains that you have already registered!
    See https://forums.aws.amazon.com/thread.jspa?threadID=91629 for more info.
    """

if __name__ == "__main__":
    # Do resource destruction
    if check_prefix_against_protected(prefix, protected_prefixes): # return True if we have a protected prefix
        print "oops, you are not allowed to delete items with that prefix"
        sys.exit()
    else:
        delete_prefixed_queues(prefix)
        delete_prefixed_buckets(prefix)
        delete_domain(prefix)

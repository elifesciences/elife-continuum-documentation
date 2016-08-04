import pytest
#  from aws_setting_utils import s3_buckets, prefix, region
# creation functions
from create_aws_resources import generate_sqs_policy
from create_aws_resources import generate_bucket_arn_from_name
from create_aws_resources import create_bucket
from create_aws_resources import create_prefixed_buckets
from create_aws_resources import create_prefixed_swf_domain
# descruciton functions
from destroy_aws_resources import get_prefixed_buckets
from destroy_aws_resources import check_prefix_against_protected
from destroy_aws_resources import check_candidates_against_protected
from destroy_aws_resources import delete_bucket
from destroy_aws_resources import delete_prefixed_buckets
# setting config functions
from moto import mock_s3
import boto3

def test_generate_bucket_arn_from_name():
    assert generate_bucket_arn_from_name("hello") == "arn:aws:s3:*:*:hello"


def test_generate_sqs_policy_json():
    test_json = {  "Version": "2012-10-17",
                    "Id": "test_sqs/SQSDefaultPolicy",
                    "Statement": [
                          {
                            "Sid": "",
                            "Effect": "Allow",
                            "Principal": {
                              "AWS": "*"
                            },
                            "Action": "SQS:SendMessage",
                            "Resource": "test_sqs",
                            "Condition": {
                                "ArnLike": {
                                "aws:SourceArn": "test_bucket"
                                }
                            }
                        }
                    ]
                }
    result = generate_sqs_policy("test_sqs", "test_bucket")
    print result 
    assert generate_sqs_policy("test_sqs", "test_bucket") == test_json


def test_positive_check_prefix_against_protected():
    prefix = 'this'
    protected = ["this", "that", "other"]
    result = check_prefix_against_protected(prefix, protected)
    assert result == True

def test_negative_check_prefix_against_protected():
    prefix = 'this'
    protected = ["that", "other"]
    result = check_prefix_against_protected(prefix, protected)
    assert result == False
#
# @mock_s3
# def test_create_bucket():
#     s3 = boto3.resource('s3')
#     bucket_name = "test_moto_bucket"
#     location = "us-east-1"
#     assert create_bucket(s3, bucket_name, location) == True
#
#     location = "eu-central-1"
#     assert create_bucket(s3, bucket_name, location) == True
#
# @mock_s3
# def test_get_prefixed_bucket():
#     # setup via creating some test buckets
#     s3 = boto3.resource('s3')
#     s3.create_bucket(Bucket="pfa-test_moto_bucket1")
#     s3.create_bucket(Bucket="pfa-test_moto_bucket2")
#     s3.create_bucket(Bucket="pfa-test_moto_bucket3")
#     s3.create_bucket(Bucket="pfb-test_moto_bucket4")
#     s3.create_bucket(Bucket="pfb-test_moto_bucket5")
#     for b in s3.buckets.all():
#         print b
#     test_prefix = "pfb"
#     test_bucket_list = ["pfb_test_moto_bucket4", "pfb_test_moto_bucket5"]
#     prefixed_buckets = map(lambda x: x.name, get_prefixed_buckets(test_prefix))
#     print prefixed_buckets
#     assert prefixed_buckets == test_bucket_list

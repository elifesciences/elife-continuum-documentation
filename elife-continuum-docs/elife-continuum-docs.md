# eLife Continuum

## Introduction

## High Level Overview

## Troubleshooting

## Doing Silent Updates


![silent corrections workflow][sc-workflow]

[sc-workflow]: https://raw.githubusercontent.com/elifesciences/ppp-project/continuum-user-docs/elife-continuum-docs/silent-updates-workflow.jpg


### Where do my files go?

### Common errors, and overcoming them

#### Dashboard article preview links are truncated.

Occasionally you may see a `The requested URL was not found on the server.` error when trying to view the processing history of an article on the dashboard. Check the link, and if the link looks like The requested URL was not found on the server.``

#### Feeding an article into the system using `ppp-feeder`

[`ppp-feeder`](https://github.com/elifesciences/ppp-feeder) is a small python script that sends a JSON message into a SQS queue which triggers an AWS SWF workflow. This workflow looks in the S3 bucket that is passed to ppp-feeder for a zip file with the key that is passed to ppp-feeder. This article zip file if found is then processed by the eLife Continuum publishing workflow. It can be used to inject an article into the publishing workflow form any S3 bucket that the user has read access on. It is highly useful in re-starting a workflow if it has gotten stuck in Continuum.

To run `ppp-feeder` you need to have python installed. Dependencies are managed using `pip` ([install pip](https://pip.pypa.io/en/stable/installing/)) and we encourage you to run `ppp-feeder` from within a [virtual env](https://virtualenv.readthedocs.org).

To run you will need to have AWS credentials that can access the S3 buckets where the articles are, and also access the
workflows that you need to feed.

You will also need to set the AWS_DEFAULT_REGION so that `ppp-feeder` knows where to look for resources.

#### `ppp-feeder` usage

ppp-feeder.py [options] bucket_name workflow_starter_queue_name, e.g.

Options:

*  -h, --help  - show this help message and exit
*  -p PREFIX, --prefix=PREFIX   - only feed keys with the given prefix
*  -r RATE, --rate=RATE  - how many seconds between messages
*  -f FILTER, --filter=FILTER  - filter regex to match against keys
*  -w, --working - print a . character for each key fed

#### `ppp-feeder` quickstart

Getting `ppp-feeder` and setting it up. Depending on the permissions on you system
you may need to run some of the commands as `sudo`.  

	$ git clone https://github.com/elifesciences/ppp-feeder.git
	$ cd ppp-feeder
	$ virtualenv ppp-feeder
	$ pip install -r requirements.txt
	$ export AWS_DEFAULT_REGION=us-east-1
	$ export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
	$ export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY

Running

	$ `ppp-feeder` ppp-feeder.py -p elife-10856-vor-r4 -r 1  elife-production-final workflow-starter-queue



#### Feeding an article into the system using an AWS bucket

#### Feeding an article into the system using the SWF console

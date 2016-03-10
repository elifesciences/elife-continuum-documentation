eLife Continuum

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Introduction](#introduction)
- [High Level Overview](#high-level-overview)
- [Deploying and configuring the system](#deploying-and-configuring-the-system)
- [Normal operation](#normal-operation)
	- [Preview mode](#preview-mode)
	- [Automatic mode](#automatic-mode)
- [Doing Silent Updates](#doing-silent-updates)
- [Troubleshooting](#troubleshooting)
	- [Understanding Caching in the system](#understanding-caching-in-the-system)
	- [Where do my files go?](#where-do-my-files-go)
	- [Is the system running?](#is-the-system-running)
	- [Checking system logs](#checking-system-logs)
	- [Checking workflow status in the AWS console](#checking-workflow-status-in-the-aws-console)
	- [Restarting the bot](#restarting-the-bot)
		- [Restarting the bot from within the Ec2 Instance](#restarting-the-bot-from-within-the-ec2-instance)
		- [Restarting the bot from elife-bilder](#restarting-the-bot-from-elife-bilder)
- [Common errors, and overcoming them](#common-errors-and-overcoming-them)
	- [Dashboard article preview links are truncated.](#dashboard-article-preview-links-are-truncated)
	- [Articles are not making it to the dashboard](#articles-are-not-making-it-to-the-dashboard)
- [ppp-feeder](#ppp-feeder)
	- [Feeding an article into the system using `ppp-feeder`](#feeding-an-article-into-the-system-using-ppp-feeder)
	- [`ppp-feeder` usage](#ppp-feeder-usage)
	- [`ppp-feeder` quickstart](#ppp-feeder-quickstart)
		- [Feeding an article into the system using an AWS bucket](#feeding-an-article-into-the-system-using-an-aws-bucket)
		- [Feeding an article into the system using the SWF console](#feeding-an-article-into-the-system-using-the-swf-console)

<!-- /TOC -->

# Introduction

# High Level Overview

# Deploying and configuring the system

# Normal operation

## Preview mode

## Automatic mode


# Doing Silent Updates

It may be a requirement to replace an published article with a minor update without creating a new version number for that article. We call this process a silent updates. At the moment the workflow for doing silent updates is manual and complex.

![silent corrections workflow][sc-workflow]

[sc-workflow]: https://raw.githubusercontent.com/elifesciences/ppp-project/continuum-user-docs/elife-continuum-docs/silent-updates-workflow.jpg



# Troubleshooting

## Understanding Caching in the system

## Where do my files go?

## Is the system running?

## Checking system logs

## Checking workflow status in the AWS console

## Restarting the bot

### Restarting the bot from within the Ec2 Instance

### Restarting the bot from elife-bilder

# Common errors, and overcoming them

## Dashboard article preview links are truncated.

Occasionally you may see a `The requested URL was not found on the server.` error when trying to view the processing history of an article on the dashboard. Check the link, and if the link looks like The requested URL was not found on the server.``

## Articles are not making it to the dashboard

# ppp-feeder

## Feeding an article into the system using `ppp-feeder`

[`ppp-feeder`](https://github.com/elifesciences/ppp-feeder) is a small python script that sends a JSON message into a SQS queue which triggers an AWS SWF workflow. This workflow looks in the S3 bucket that is passed to ppp-feeder for a zip file with the key that is passed to ppp-feeder. This article zip file if found is then processed by the eLife Continuum publishing workflow. It can be used to inject an article into the publishing workflow form any S3 bucket that the user has read access on. It is highly useful in re-starting a workflow if it has gotten stuck in Continuum.

To run `ppp-feeder` you need to have python installed. Dependencies are managed using `pip` ([install pip](https://pip.pypa.io/en/stable/installing/)) and we encourage you to run `ppp-feeder` from within a [virtual env](https://virtualenv.readthedocs.org).

To run you will need to have AWS credentials that can access the S3 buckets where the articles are, and also access the
workflows that you need to feed.

You will also need to set the AWS_DEFAULT_REGION so that `ppp-feeder` knows where to look for resources.

## `ppp-feeder` usage

ppp-feeder.py [options] bucket_name workflow_starter_queue_name, e.g.

Options:

*  -h, --help  - show this help message and exit
*  -p PREFIX, --prefix=PREFIX   - only feed keys with the given prefix
*  -r RATE, --rate=RATE  - how many seconds between messages
*  -f FILTER, --filter=FILTER  - filter regex to match against keys
*  -w, --working - print a . character for each key fed

## `ppp-feeder` quickstart

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



### Feeding an article into the system using an AWS bucket

### Feeding an article into the system using the SWF console

eLife Continuum

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Introduction](#introduction)
- [High Level Overview](#high-level-overview)
- [Deploying and configuring the system](#deploying-and-configuring-the-system)
	- [using elife-builder](#using-elife-builder)
	- [using elife-builder to see what is running](#using-elife-builder-to-see-what-is-running)
	- [using elife-builder to ssh into a machine](#using-elife-builder-to-ssh-into-a-machine)
	- [using elife-builder to deploy a new instance](#using-elife-builder-to-deploy-a-new-instance)
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
		- [Restarting bot processes from within the Ec2 Instance](#restarting-bot-processes-from-within-the-ec2-instance)
		- [Redeploying the bot from elife-bilder](#redeploying-the-bot-from-elife-bilder)
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

eLife uses a project called [elife-builder](https://github.com/gnott/elife-builder) built on top of [saltstack](https://docs.saltstack.com/en/latest/topics/) for configuration and deployment of Continuum. It is our intention to open source relevant components from elife-builder, however we have not made this project available publicly yet.

elife-builder wraps commands around salt and can be used to deploy instances to
Vagrant or to Amazon Web Services.

For deployment to AWS the rules that generate the  url that the service is made available from is defined in the [top.sls](https://github.com/gnott/elife-builder/blob/master/salt/salt/top.silent-updates-workflow) file. This file also defines which salt configurations are applied to a
machine.

For a specific project, the instructions for building that machine are set in
a project specific folder within the salt project, so to configure the elife-bot
we use and [elife-bot/init.sls](https://github.com/gnott/elife-builder/blob/master/salt/salt/elife-bot/init.sls) file.

This is also where cron jobs for this system are configured, and deployed to the
target machine.

This file instructs the machine that is built to deploy the project's python settings
file, which is also kept under revision in the salt project at [elife-bot/config/opt-elife-bot-settings.py](https://github.com/gnott/elife-builder/blob/master/salt/salt/elife-bot/config/opt-elife-bot-settings.py).

Crucially this system is set to refresh and overwrite settings on all host machines
once a day. This forces us to keep all system configuration in code and prevents
customisation happening on the machine.

elife-builder exposes some high level commands to the user for deploying, managing and
tearing down instances. AWS keys with appropriate permissions need to be set on the
machine of the user.

## using elife-builder

elife-builder is a wrapper for [fabric](http://www.fabfile.org), so in addition to being
able to issue fabric commands, builder also provides some elife specific commands

The elife specific commands can be listed with

	$ ./bldr -l

## using elife-builder to see what is running

	$ ./bldr aws_stack_list

This will list running stacks on AWS. You should expect to see the following services running:

* elife-bot-*
* elife-dashbarod-*
* elife-lax-*
* elife-metrics-*
* elife-api-*

If any of these are missing something is wrong.

## using elife-builder to ssh into a machine

All of the services listed with `./bldr aws_stack_list` are Ec2 instances running
on AWS. elife-builder provides a command to allow you to easily ssh into one of these
instances, though this is not recommended.

	$ ./bldr ssh

This will return a list of available machines that you can ssh into. Pick the machine of
interest from the list.

## using elife-builder to deploy a new instance



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

### Restarting bot processes from within the Ec2 Instance

The bot needs a number of python process to be running to function properly. If any of these processes go AWOL then things will break. You can restart these processes manually
from within the Ec2 instance, though this is not recommended.

First ssh into the machine where you suspect that there might be problem:

	$ ./bldr ssh

Check to see if the process that you expect are running:

	elife@ip-10-0-2-237:~$ ps -aux | grep "python"  

You should see the following process in operation:

	python decider.py  
	python worker.py  
	python queue_worker.py  
	python queue_workflow_starter.py  

If any of these are missig then there is a problem. To restart the required python processes do the following:L

	elife@ip-10-0-2-237:~$ killall -u elife python  
	elife@ip-10-0-2-237:~$ cd /opt/elife-bot && /opt/elife-bot/scripts/run_env.sh live
	


### Redeploying the bot from elife-bilder

If you need to tear down the bot, and create a totally new instance, you can do this using elife-builder, though we have not tested this on the production environment yet, so you should probably not try this.

 	$ ./bldr aws_delete_stack

Then pick the stack that you want to delete.

	$ ./bldr aws_launch_instance

This will sync a set of cloudformation templates to your machine from AWS S3 and provide you with a known list of services that can be created. Pick from the list, and provide
the appropriate postfix for the service name.

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

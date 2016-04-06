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
	- [Understanding timeouts in the system](#understanding-timeouts-in-the-system)
	- [Where do my files go?](#where-do-my-files-go)
	- [Is the system running?](#is-the-system-running)
	- [Checking system logs](#checking-system-logs)
	- [Checking workflow status in the AWS console](#checking-workflow-status-in-the-aws-console)
	- [Restarting the bot](#restarting-the-bot)
		- [Restarting bot processes from within the Ec2 Instance](#restarting-bot-processes-from-within-the-ec2-instance)
		- [Redeploying the bot from elife-bilder](#redeploying-the-bot-from-elife-bilder)
- [Common errors, and overcoming them](#common-errors-and-overcoming-them)
	- [Dashboard article preview links are truncated.](#dashboard-article-preview-links-are-truncated)
	- [Drupal is returning a 429 error on the PostEIF workflow step](#drupal-is-returning-a-429-error-on-the-posteif-workflow-step)
	- [Drupal is returning a 500 error on the PostEIF workflow step](#drupal-is-returning-a-500-error-on-the-posteif-workflow-step)
	- [Drupal is returning a 503 error on the PostEIF workflow step](#drupal-is-returning-a-503-error-on-the-posteif-workflow-step)
	- [Drupal is returning a `message:('Connection aborted.', BadStatusLine("''",))" `on the PostEIF workflow step](#drupal-is-returning-a-messageconnection-aborted-badstatusline-on-the-posteif-workflow-step)
	- [Articles are not making it to the dashboard](#articles-are-not-making-it-to-the-dashboard)
- [ppp-feeder](#ppp-feeder)
	- [Feeding an article into the system using `ppp-feeder`](#feeding-an-article-into-the-system-using-ppp-feeder)
	- [`ppp-feeder` usage](#ppp-feeder-usage)
	- [`ppp-feeder` quickstart](#ppp-feeder-quickstart)
		- [Feeding an article into the system using an AWS bucket](#feeding-an-article-into-the-system-using-an-aws-bucket)
		- [Feeding an article into the system using the SWF console](#feeding-an-article-into-the-system-using-the-swf-console)
- [Deploying a test instance of Continuum using elife-builder](#deploying-a-test-instance-of-continuum-using-elife-builder)
	- [Useful builder commands](#useful-builder-commands)
	- [Deploying an instance with builder](#deploying-an-instance-with-builder)
		- [Fixing builder2 issues with let's encrypt](#fixing-builder2-issues-with-lets-encrypt)
	- [Deploying a test instance of the elife website.](#deploying-a-test-instance-of-the-elife-website)
	- [Deploying an instance of lax](#deploying-an-instance-of-lax)
	- [Deploying an instance of the dashboard with custom configuration](#deploying-an-instance-of-the-dashboard-with-custom-configuration)
	- [Deploying a custom instance of the bot](#deploying-a-custom-instance-of-the-bot)
		- [A note about cron jobs with the elife-bot](#a-note-about-cron-jobs-with-the-elife-bot)
	- [Preparing and creating the required AWS resources](#preparing-and-creating-the-required-aws-resources)
		- [Creating S3 Buckets](#creating-s3-buckets)
		- [Creating the required queues](#creating-the-required-queues)
		- [Connecting our S3 buckets to our queues](#connecting-our-s3-buckets-to-our-queues)
		- [Creating the required SWF domain](#creating-the-required-swf-domain)
		- [Using a utility script to create these resources](#using-a-utility-script-to-create-these-resources)

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

## Understanding timeouts in the system

Timeouts can happen in a number of places in the system. Every activity has it's own timeout set in the workflow definition. Activities are usually set to have a timeout of five minutes, however on occasion we were observing that image conversion was taking slightly longer, and so the image conversion timeout was raised to eight minutes.

When an individual activity timeouts then SWF will restart that activity, and it will continue to do so until the workflow itself times out.  

In addition to these timeouts, the webserver will terminate HTTP connections after 60 seconds.

A consequence of this is that for the workflow which sends a message to Drupal instructing Drupal to create a new article, if the Drupal process takes longer than 60 seconds to do this then the activity will receive an error message from the webserver, even though the process on Drupal has not failed. The workflow activity is still under it's own timeout and it will continue to retry sending a message to Drupal. We have noticed that if Drupal is able to process multiple connections this situation can lead to unexpected consequences, and errors in publishing content. As a result we have setup Drupal to only ingest articles sequentially and to refuse requests while the ingest process is happening.

![system timeouts][system-timeouts]

[system-timeouts]:https://raw.githubusercontent.com/elifesciences/ppp-project/continuum-user-docs/elife-continuum-docs/continuum-timeouts.jpg

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

Occasionally you may see a `The requested URL was not found on the server.` error when trying to view the processing history of an article on the dashboard. Check the link, and
if the link looks like The requested URL was not found on the server.``

## Drupal is returning a 429 error on the PostEIF workflow step  

Drupal is busy processing another request. Usually the solution to this is to wait wait as the POST EIF activity will continue to retry for up to five minutes. If the article fails to get through to Drupal within this window you will need to re-run this workflow.

![429 error][429]

[429]: https://raw.githubusercontent.com/elifesciences/ppp-project/continuum-user-docs/elife-continuum-docs/429-error.png


## Drupal is returning a 500 error on the PostEIF workflow step  

Presently it's unclear what is causing these errors, it is probably judicious to check the health of the Drupal instance before reposting the article, as there may be some identifiable issue with Drupal, such as a specifically slow database query.


## Drupal is returning a 503 error on the PostEIF workflow step  

The Drupal server is unavailable,usually a deploy is in progress, the boot will retry for five minutes, and if it does not success within that window, wait for the deploy to be complete and restart the workflow.

## Drupal is returning a `message:('Connection aborted.', BadStatusLine("''",))" `on the PostEIF workflow step  

This indicates that our webserver has timed out. The process of ingestion is continuing on the Drupal side, but this is of no help to the elife bot, which, like a forlorn lover, is going to continue to send missives of hope to Drupal. At this point any number of issues might arise, but your best hope is that in the course of resending a publication message to Drupal, the next request comes in after Drupal has completed the previous request, and this request completes in under 60 seconds, and no articles are unpublished or corrupted in the process.

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


# Deploying a test instance of Continuum using elife-builder

`elife-builder` is a project that is used for deployments within eLife. It is a wrapper for
python fabric, and we use [http://saltstack.com]() for configuration management. We use Amazon Cloud Formation templates for deploying machines on the amazon cloud. It is under rapid development
and this documentation refers to the [ctdocs-master-v1](https://github.com/elifesciences/elife-builder/tree/ctdocs-master-v1) tag for code on the master branch, and the [ctdocs-v1](https://github.com/elifesciences/elife-builder/tree/ctdocs-v1) for code that is being developed on the [feature-bldr2](https://github.com/elifesciences/elife-builder/tree/feature-bldr2) branch.

Builder knows about projects that are defined in the [top.sls](https://github.com/elifesciences/elife-builder/blob/master/salt/salt/top.sls) file. For our purposes a project is all of the configuration information needed to build a server that can run a service. These projects have their specific detailed configuration image-information defined in salt under the [salt/salt/]
(https://github.com/elifesciences/elife-builder/tree/master/salt/salt/) directory (e.g. this is our configuration for jira) [elife-jira](https://github.com/elifesciences/elife-builder/tree/master/salt/salt/elife-jira). These instance specific configurations can also inherit from a base configuration, making it tractable to define common pieces of infrastructure, like logging infrastructure.

## Useful builder commands

  $ ./bldr aws_stack_list

Will list all running ec2 instances that have been created with builder.

  $ ./bldr ssh

Will provide options for ssh'ing into any given machine.

## Deploying an instance with builder

Builder provides the `aws_launch_instance` command to create ad-hoc project instances on AWS.
When using this command an "instance ID" is required that will uniquely identify this instance from all other instances of this project. The instance ID is suffixed to the project name. The instance ID of `test` for the `elife-website` for example will form the identifier `elife-website-test`.
This command is able to launch any project but *not* branches of projects that are tied to a repository.

Builder does provide the `deploy` command that will allow the creation of instances of a project specific to it's github branch names.

The `deploy` command does not support multiple instances of the same branch. To deploy multiple intances of the code in a branch, clone that branch into a new branch and deploy that.

For example, if we wanted to deploy a different branch of lax we would need to modify the [init.sls file here](https://github.com/elifesciences/elife-builder/blob/ctdocs-master-v1/salt/salt/elife-lax/init.sls#L9) to point to a specific named branch. If we wished to deploy a different branch of the elife dashboard we would either need to modify [init.sls here](https://github.com/elifesciences/elife-builder/blob/ctdocs-master-v1/salt/salt/elife-dashboard/init.sls#L11), or we would need to provide a custom `.sls` file that overrode the information ind `init.sls`.

We will look at examples of both methods for bringing up parts of the continuum infrastructure.

### Fixing builder2 issues with let's encrypt

Currently there is an issue with let's encrypt, and when deploying via the `build` command, builds fail. To overcome this you can manually resolve this issue on the machine, and then manually restart the salt deploy.

Ssh into the machine affected and from there do the following:
----
>   
  $ cd /opt/letsencrypt/
  $ git reset --hard
  $ sudo salt-call state.highstate


## Deploying a test instance of the elife website.

In order to deploy to AWS builder uses cloudformation, and so when deploying we need to create the stack template, and then deploy that stack template.

If you wish to just create the cloudformation stack without launching it then use `./bldr create_stack`. To both create and launch a stack use `./bldr aws_launch_instance`.

If the project uses a webserver, it will probably be available at instancename.sub.elifesciences.org. For example, an instance of the lax project called branch-foo when deployed will be available at branch-foo.lax.elifesciences.org. The routing is defined in [/projects/elife.yaml](uri-config).

For this test we are going to use the instance suffix `continuum-test`.

To launch an instance of the elife website do the following

>   
	bldr aws_launch_instance

You will be asked to choose from projects that builder knows about:

>   
	please pick a known project:
	1 - basebox
	2 - builder-builder
	3 - central-logging
	4 - elife-api
	5 - elife-dashboard
	6 - elife-jira
	7 - lagotto
	8 - elife-bot
	9 - elife-bot-large
	10 - master-server
	11 - elife-civiapi
	12 - elife-ci
	13 - elife-crm
	14 - elife-website
	15 - elife-website-medium
	16 - elife-arges
	17 - elife-lax
	18 - elife-lax-nonrds
	19 - elife-metrics

Pick the `elife-website` project and provide the instance id (our suffix)
 that we want. It defaults to giving an instance id based off of today's date. For this example we will enter `continuum-test` and hit return.

>   
	 > ('elife-website') 14
	 instance id [2016-03-29]:
	 > continuum-test

Looking in [/projects/elife.yaml](uri-config) we [see that the namespace for the website is `v2`](https://github.com/elifesciences/elife-builder/blob/master/projects/elife.yaml#L231):

>    
	elife-website:
	    subdomain: v2 # v2.elifesciences.org
	    aws:
	        ports:
	            22: 22
	            80: 80

so our `continuum-test` version of the website will be available at [http://continuum-test.v2.elifesciences.org]().

This will also sync a copy of the backup DB into Drupal, and brining up this instance took about five minutes.

The path to the CDN is hard coded in this instance, but we can override this from the Drupal management screen. To access the site you can use the `drush uli` command to generate an admin login token, and then go to the following admin screen [http://continuum-test.v2.elifesciences.org/admin/config/services/elife-article-assets-source](). You can configure the path to the CDN from this page. This is important if you are testing your system with a version of the bot that pushes content into a test CDN location.


## Deploying an instance of lax

>  
		$ ./bldr aws_launch_instance

Provide the `continuum-test` as the instance name, and lax is now available at

[uri-config]: https://github.com/elifesciences/elife-builder/blob/master/projects/elife.yaml


## Deploying a custom instance of the bot

Configuration for the bot is slightly different. Rather than telling salt to point to a specific custom settings file, we modify the settings file in place, and we add a new class in that settings file that is used by the bot when the bot is run.

We need to add that class to [opt-elife-bot-settings.py](https://github.com/elifesciences/elife-builder/blob/master/salt/salt/elife-bot/config/opt-elife-bot-settings.py), and it should contain pointers to the new instances of `lax`, and the `elife-website` that we have just brought up. It should also point to the appropriately named AWS resources, so for this example we should expect to see the following in this class

>      sqs_region = 'us-east-1'
    S3_monitor_queue = 'ct-incoming-queue'
    event_monitor_queue = 'ct-event-property-incoming-queue'
    workflow_starter_queue = 'ct-workflow-starter-queue'
    workflow_starter_queue_pool_size = 5
    workflow_starter_queue_message_count = 5


>       # S3 settings
    publishing_buckets_prefix = 'ct-'
    # shouldn't need this but uploads seem to fail without. Should correspond with the s3 region
    # hostname list here http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
    s3_hostname = 's3.amazonaws.com'
    production_bucket = 'elife-production-final'
    eif_bucket = 'elife-publishing-eif'
    expanded_bucket = 'elife-publishing-expanded'
    ppp_cdn_bucket = 'elife-publishing-cdn'
    archive_bucket = 'elife-publishing-archive'
    xml_bucket = 'elife-publishing-xml'

>      # REST endpoint for drupal node builder
    # drupal_naf_endpoint = 'http://localhost:5000/nodes'
    drupal_EIF_endpoint = 'http://continuum-test.v2.elifesciences.org/api/article.json'
    drupal_approve_endpoint = 'http://continuum-test.v2.elifesciences.org/api/publish/'


>     # lax endpoint to retrieve information about published versions of articles
    lax_article_versions = 'https://continuum-test.lax.elifesciences.org/api/v1/article/10.7554/eLife.{article_id}/version/'
    lax_update = 'https://continuum-test.lax.elifesciences.org/api/v1/article/create-update/'

When building the bot, builder does not launch the bot, so currently in order to run the bot you need to ssh into the bot machine, and launch the bot manually.

Before running the bot we need to register all of the Amazon SWF workflows:

>   
  $ cd /opt/elife-bot
  $ python register.py

Now we can run the bot processes.

>   
  $ cd  /opt/elife-bot
  $ ./scripts/run_env.sh continuum

(note this script has to be run from the parent drectory).

We pass the class name that contains the instance specific settings, in order for the bot to start with those settings.

We expect the see the following running:

> decider.py
> worker.py
> queue_worker.py
> queue_workflow_starter.py


### A note about cron jobs with the elife-bot

Some workflows in the publishing system require a cron job to run to periodically
check for inbound articles. The cron jobs are not currently configured through the builder.

It would be good to ensure that the following cron jobs are enabled:

>
  */5 * * * * cd /opt/elife-bot && /opt/elife-bot/scripts/run_cron_env.sh live
  27 * * * * killall -u elife python && cd /opt/elife-bot &&
  /opt/elife-bot/scripts/run_env.sh

`run_cron_env.sh live` runs every five minutes to ...
`run_env.sh` runs every hour to restart the machine because `reasons`


## Deploying an instance of the dashboard with custom configuration

Configuration for our projects is determined by salt. Salt uses yaml files to find the configuration files, and project configuration is held in the builder repository rather than in the project specific repo. Salt can be configured to set different configuration based on project name, and this provides a nice way to manage alternative configurations for live or development environments.

[top.sls](https://github.com/elifesciences/elife-builder/blob/master/salt/salt/top.sls) is where this routing is done, and if you examine the section for the dashboard project you can see that currently there are two sets of configurations defined:

>   
	'elife-dashboard-*':
		- base.daily-system-updates
		- base.python-dev
		- base.postgresql
		- base.nginx
		- base.uwsgi
		- base.acme
		- elife-dashboard
		- elife-dashboard.uwsgi
	'elife-dashboard-parallel':
		- elife-dashboard.parallel

The `elife-dashboard-*` config setting will catch all instances that match elife-dashboard. The
`elife-dashboard` directive requires an `init.sls` config file to be in the project directory.
You can omit a directive like `elife-dashboard`, but you cannot have a `elife-dashboard` directive without the `init.sls` file.

the `elife-dashboard-parallel` settings will only be applied to instances that match that name.

To create a custom config for our `continuum-test` namespace we just need to add a new routing setting here:

>   
	'elife-dashboard-*':
		- base.daily-system-updates
		- base.python-dev
		- base.postgresql
		- base.nginx
		- base.uwsgi
		- base.acme
		- elife-dashboard
		- elife-dashboard.uwsgi
 	'elife-dashboard-continuum-test':
		- elife-dashboard.continuum-test
	'elife-dashboard-parallel':
		- elife-dashboard.parallel

These directives point to `.sls` files held in the project specific directory of salt, and those `.sls` files are where the location of the specific configuration files are set.

To make `elife-dashboard.continuum-test` active we need a corresponding `continuum-test.sls` file in the `/salt/salt/elife-dashbard/` directory. This file will point to a `salt/salt/elife-dashboard/config/srv-app-dashboard-continuum-test_settings.py` file, and it is in this file that we can define our custom AWS settings for this instance.

`srv-app-dashboard-continuum-test_settings.py`:

>   
	{% set app = pillar.elife_dashboard %}
	preview_base_url = 'http://continuum-test.v2.elifesciences.org/'
	# RDS settings
	rds_region = 'us-east-1'
	# SQS settings
	sqs_region = 'us-east-1'
	event_monitor_queue = 'ct-event-property-incoming-queue'
	workflow_starter_queue = 'ct-workflow-starter-queue'
	event_queue_pool_size = 5
	event_queue_message_count = 5
	# Logging
	log_level = "WARN"
	log_file = "/var/log/app.log"
	process_queue_log_file = "/var/log/process-queue.log"
	# Database
	database = "{{ app.db.name }}"
	host = "{{ salt['elife.cfg']('cfn.outputs.RDSHost') or app.db.host }}"
	port = "{{ salt['elife.cfg']('cfn.outputs.RDSPort') or app.db.port }}"
	user = "{{ app.db.username }}"
	password = "{{ app.db.password }}"

We can now bring up this instance with:

>  
	./bldr aws_launch_instance

This will bring up a dashboard instance at `[http://continuum-test.ppp-dash.elifesciences.org/]()`. (note, currently any infrastructure that is RDS backed will take some time to come up).

You can verify that the correct instance of the dashboard has been created by ssh'ing into the machine, and

>
	$ cd /srv/app/dashboard/
	$ grep "event_monitor_queue" settings.py
	event_monitor_queue = 'ct-event-property-incoming-queue'

You should see the same queue name as the one provided in the setting file of the builder repo.

### bringing up an instance of the dashboard

We have deployed an instance of the dashboard, however it is not yet communicating with the queues that it needs to receive the info to display on the dashboard, nor to the queues that it needs to send the signal for publishing to Drupal.

To start the process that consumes feeds:

>   
  $ cd /srv/elife-dashboard
  $ python process_dashboard_queue.py &

To get the dashboard to communicate with the outbound queus, there is currently a bug that prevents the nginx process from reading the correct aws permissions, so until that if fixed you can manually copy the `.aws` directory from `/home/elife/.aws` to `/var/www/.aws`. /var/www is the home folder for the www-data user.

### Restarting the dashboard

The dashboard flask app is run under `nginx`. To restart that process you need to restart it via `etc/init.d/uwsgi-app`.

### Updating the dashboard

Updating any instance is now easily done with the `./bldr deploy` comannd. Run that command and pick the instance that you want to have updated. You will need to pick the porject name and then the branch name. You can also update an instance with the `./bldr aws_update_instance` command. This will provide a list of running instances to choose from for updating.



## Preparing and creating the required AWS resources

Our publishing infrastructure runs off of AWS. Services use amazon S3 to store articles in different processing states, as well as storing other artifacts, such as the article XML, and as the location of the CDN for content on the live site. We uses SQS to provide queues for communicating between services, and we use Amazon Simple Workflow to coordinate the activities of the publishing bot.




The appropriate resources need to be created in AWS before the publishing system can run.



### Creating S3 Buckets

The elife-bot [requires the following buckets](# https://github.com/elifesciences/elife-builder/blob/master/salt/salt/elife-bot/config/opt-elife-bot-settings.py#L25-L27) to exist:

>      
    production_bucket = 'elife-production-final'
    eif_bucket = 'elife-publishing-eif'
    expanded_bucket = 'elife-publishing-expanded'
    ppp_cdn_bucket = 'elife-publishing-cdn'
    archive_bucket = 'elife-publishing-archive'
    xml_bucket = 'elife-publishing-xml'

Here the variable name is internal to the code and the value should be the name of an actual bucket in your AWS infrastructure.

The elife-bot code takes a variable for a [bucket prefix](https://github.com/elifesciences/elife-builder/blob/master/salt/salt/elife-bot/config/opt-elife-bot-settings.py#L32), so if you include a prefix here the code will look for AWS S3 buckets that have the name provided in this setting with the addition of this prefix. E.g. if you provide the prefix `exp-` the bot code will look for buckets like `exp-elife-publishing-cdn` etc. This is a handy way to create different resources for testing or production.

### Creating the required queues

The publishing dashboard requires the [following queues](https://github.com/elifesciences/elife-builder/blob/master/salt/salt/elife-dashboard/config/srv-app-dashboard-prod_settings.py#L9-L11) to be created:

>  
  sqs_region = 'us-east-1'
  event_monitor_queue = 'event-property-incoming-queue'
  workflow_starter_queue = 'workflow-starter-queue'

The elife-bot requires the [following queues](https://github.com/elifesciences/elife-builder/blob/master/salt/salt/elife-bot/config/opt-elife-bot-settings.py#L25-L27) to be created:

>       
  S3_monitor_queue = 'incoming-queue'
  event_monitor_queue = 'event-property-incoming-queue'
  workflow_starter_queue = 'workflow-starter-queue'

The code that looks for queues does not have the ability to specify a prefix. This is an inconsistency that we aim to resolve in a later release.

### Connecting our S3 buckets to our queues

The publishing system in Continuum reacts when a new article arrives. The way it does this is that
S3 buckets can trigger events that can be pushed onto a queue. We trigger an event eery time a new article arrives in a specified bucket, and this populates a queues that the publishing system is listening to. When the publishing system sees that a new article has arrived it triggers the publishing process.

To enable this we need to turn on bucket notifications for the , and

the bucket needs to have the following permissions

aws: list, update/delete, view permissions, edit permissions

>   
  notifications need to be set to:
  have a name: NewS3Object
  events: ObjectCreated (All)
  SQSqueue
  queue name: incoming-queue

The appropriate queue needs to have a policy like the following assigned to it:

>   
  {
    "Version": "2012-10-17",
    "Id": "arn:aws:sqs:us-east-1:512686554592:incoming-queue/SQSDefaultPolicy",
    "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
          "AWS": "*"
        },
        "Action": "SQS:SendMessage",
        "Resource": "arn:aws:sqs:us-east-1:512686554592:incoming-queue",
        "Condition": {
          "ArnLike": {
            "aws:SourceArn": "arn:aws:s3:*:*:elife-production-final"
          }
        }
      }
    ]
  }




### Creating the required SWF domain

The bot communicates with Amazon Simple Work Flow, which is a workflow management system. SWF has a concept called domains. These domains provide namespaces within which workflows can operate. We can create instances of our publishing system that operate within different domains, and this ensures that different environments will not interfere with each other.

Domains can be created from the SWF console, and they can also be created using AWS command line utilities or SDKs.

If we have a prefix `ct` that we want to use to create a domain the following `boto3` code will do that for us

>        
    swf = boto3.client('swf')
    prefix = `ct`
    swf.register_domain(name="Publish" + "." + prefix, description="test SWF domain for thie



### Using a utility script to create these resources



# Gotcha's

## Let's Encrypt SSL issue on test instances

Instances get deployed with a staging SSL certificate that expires after three months. You may encounter calls from the `requests` library failing. If this happens, then you need to issue a new
certificate to the istance that is failing.

### cloning and pushing a branch
git push --set-upstream origin MyLocalBranch

### Setting credentials for the dashboard to enable it to publish.

### Using this system for testing branches

We now have a complete deploy of the test system. We are deploying via branch name, and
for the dashboard we are using the branch name `continuum-test`. This is tied to a specific
configuration file that will connect this instance to the approriatly named AWS resources, and
the test site.

If we now want to test a feature within this enviornment it should be possible to replace our
branch with a checkout of the feature branch that we are interested in deploying. We should
then be able to use the builder update command to redeploy that instance, and it will pulldown the
new code. We will need to remember to manually restart any services that are requried.

Let's go ahead and deploy the develop branch of the dashboard to the `continuum-test` instance.

First we get rid of the remote branch `continuum-test` on github:

>
  $ git push origin --delete continuum-test
  remote: This repository moved. Please use the new location:
  remote:   https://github.com/elifesciences/elife-dashboard.git
  To https://github.com/digirati-co-uk/elife-dashboard
   - [deleted]         continuum-test

Now we delete that branch locally

>   
  $ git branch -d continuum-test
  Deleted branch continuum-test (was 939aa87).

Now we checkout a copy of deploy as continuum-test locally

> $ git branch -d continuum-test
Deleted branch continuum-test (was 939aa87).
git checkout develop
Branch develop set up to track remote branch develop from origin.
Switched to a new branch 'develop'
➜  elife-dashboard git:(develop) git checkout -b continuum-test
Switched to a new branch 'continuum-test'
➜  elife-dashboard git:(continuum-test)

Now we push this new branch back up to github

>   
  $ git push --set-upstream origin continuum-test
  Total 0 (delta 0), reused 0 (delta 0)
  remote: This repository moved. Please use the new location:
  remote:   https://github.com/elifesciences/elife-dashboard.git
  To https://github.com/digirati-co-uk/elife-dashboard
   * [new branch]      continuum-test -> continuum-test
  Branch continuum-test set up to track remote branch continuum-test from origin.

We can now redeploy the elife-dashboard, and it should deploy this version of the code.

A word of warning, I did try to update the stack using `aws_update_stack`, but that didn't work.
In order to back out from that I deleted the stack using `aws_delete_stack` and then deployed the
branch using `./bldr deploy` and selecting the `continuum-test` branch. This succedded in getting the code from the deploy branch onto the continuum-test instance.

# Summarised deployment guide

Note, after ssh'ing into any given project you may need to run `sudo pip install -r requirements.txt` from within the project directory, depending on whether project depencies have been deployed correctly.

You may need to update your version of builder from within the elife builder project vis:

  $ git pull
  $ ./update.sh

Deploy the aws resources. (still a bit buggy)

  $ python create_s3_resources.py -p `your_test_prefix`

in this case our test prefix is going to be `ct`, short for `continuum-test`.

You now need to make the CDN bucket an actual CDN, log in to your AWS console and go to the
`` bucket.

Deploy a test instance of lax from within the builder project

  $ cd ~/lax_directory
  $ git checkout master -b continuum-test
  $ git push --set-upstream origin continuum-test
  $ cd ~/elife_builder
  $ ./bldr deploy

(pick the elife-lax) project and pick the continuum-test branch for deployment.

Now we deploy an instance of the elife website, from within the builder project

  $ ./bldr aws_launch_instance

Pick the elife-website project and provide the `continuum-test` suffix

ssh in to the machine to create an admin login via drush

  $ ./bldr ssh

(the default option should be for the website instance that you have just brought up, and you will now be inthat instance.

    ~> drush uli

Log in to the Drupal instance via the url provided, and go to the following screen

[http://continuum-test.v2.elifesciences.org/admin/config/services/elife-article-assets-source]()

Enter the value of the CDN that was set in the AWS console.

Now we deploy an instance of the bot from within the builder project

We need to configure our settings for the bot to be specific to this test instance.

  $ cd ~/elife_builder/salt/salt/elife-bot/config

edit the file `opt-elife-bot-settings.py` and add a new class that encapsulates the settings that you need for communicating with the new aws resources created earlier. Commit these changes. Now
launch an instance of the bot. Make a note of the class name as this will be needed to launch this instance of the bot.

  $ ./bldr aws_launch_instance

Pick the elife-bot project, and provide the suffix, then after the machine has been built, ssh into the machine. After ssh'ing in we will register the SWF workflows, and then we will start the bot processes.

  $ ./bldr ssh
  ~> cd cd /opt/elife-bot
  ~> python register.py
  ~> ./scripts/run_env.sh continuum

Now we launch an instance of the dashboard, we need to modify the dashboard settings to point to the approriate endpoints. From within the builder project

  $ cd ~/elife_builder/salt/salt 

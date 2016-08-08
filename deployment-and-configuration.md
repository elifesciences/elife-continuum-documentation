** DRAFT, NOT YET FULLY TESTED **

eLife continuum is currently deployed within eLife's AWS infrastructure. This guide will outline how to install the system on your own AWS infrastructure using  [https://github.com/elifesciences/builder](https://github.com/elifesciences/builder).

As of writing this deployment recipe is incomplete, and will probably not lead to success, but we are actively working on getting this into a usable state ASAP and expect to have a Jenkins build pipeline ready soon.

# Configuring the SWF domain that the bot is running under.

SWF supports different domains. These are namespaces, and they can be used to run different production or test environments of the bot. SWF only allows you to create up to 100 domains, so do not use them with abandon.

Before running, workflows and activities need to be registered with SWF. This is done by running the [register.py](https://github.com/elifesciences/elife-bot/blob/develop/register.py) script.

This script takes an argument name which should match the domain that you want the bot to run under. It defaults to `dev`. At the same time the register.py script will pull in settings from [settings.py](https://github.com/elifesciences/elife-bot/blob/develop/settings-example.py), based on the domain name passed in as an argument. It does this via a class in the settings file.

The builder project can be configured to set the argument that register.py receives. This is done in the [elife-bot-formula](https://github.com/elifesciences/elife-bot-formula/blob/master/salt/elife-bot/init.sls#L228) repo, and the actual value is set in the `builder-private/pillar/environment-prod.sls` file.

At the same time as all of this, the actual domain that you want needs to be setup in SWF. This can be done by running `create_aws_resources.py` while setting the domain parameter in `continuum.yaml`. This will also setup buckets and queues that are prefixed with the same domain name. This is not a requirement, but we have found it helpful if you are running the bot on more that one domain within one AWS region. It means you can quickly navigate to a specific AWS bucket for a given workflow, just by looking at the name of the bucket.

In

So to change the name of the domain that you operate under you need to:

* create the domain (ideally by setting the domain parameter in `continuum.yaml` and running the create resources script)  
* create a class in the settings.py file for the bot that matches the domain you want to use  
* modify the parameter that `register.py` takes on running  
* update the bot machine using builder  

At the time of writing:

* **the elife bot defaults to operating in us-central-1**
* **the `configure_continuum_settings.py` script does not set the argument for register.py**

# System configuration

## Image File Format configuration

## Default Publishing Behaviour configuration

## Configuring default publishing workflows

Most of the workflows in continuum are triggered by a message sent into a specific Amazon SQS queue, the `workflow-starter-queue`. There is a long running process that listens to messages on this queue. If the message is in the correct format, and contains the name of a registered workflow, then `queue-workflow-starter.py` triggers that workflow.

Amazon S3 buckets can be configured to send a message to a queue if any of their content is modified. We make use of this to start the very first of the workflows. Modifications to a specific bucket are configured to send a message into a `S3_monitor_queue`. There is a long running process `queue_worker.py` that listens in to this queue. `queue_worker.py` is configured to launch a workflow defined in `newFileWorkflows.yaml`. It does this by sending a message in to `workflow-starter-queue` and the usual process takes over from there. In this way files arriving from a typesetter can automatically trigger the appropriate publication workflows, and those workflows can be configured easily by modifying `newFileWorkflows.yaml`.

** DRAFT, NOT YET FULLY TESTED **

eLife continuum is currently deployed within eLife's AWS infrastructure. This guide will outline how to install the system on your own AWS infrastructure using  [https://github.com/elifesciences/builder](https://github.com/elifesciences/builder).

As of writing this deployment recipe is incomplete, and will probably not lead to success, but we are actively working on getting this into a usable state ASAP and expect to have a Jenkins build pipeline ready soon.

# Basic AWS configuration

Before getting started with the deployment you will need to have some basic configuration setup in AWS. We have provided a couple of scripts that assist with AWS configuraiton, but the following steps currently need to be done manually:

* create an IAM user with the correct permissions  
* setup a test domain name, and configure domain management through Route 53   
* configure, or ensure that you have, a VPN and associated subnets setup  

## Creating the IAM user.

You will need a set of AWS keys. The safest way to do this is to create an IAM user and add this user to a group that has the required permissions. If you keys get compromised you can delete your user, and create a new user with new keys.

The IAM group will need the following permissions

* S3
* Ec2
* SWF
* RDS
* Route53
* custom CloufFormation policy to grant full cloud formation access

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
          "cloudformation:CancelUpdateStack",
          "cloudformation:ContinueUpdateRollback",
          "cloudformation:CreateChangeSet",
          "cloudformation:CreateStack",
          "cloudformation:DeleteChangeSet",
          "cloudformation:DeleteStack",
          "cloudformation:Describe*",
          "cloudformation:EstimateTemplateCost",
          "cloudformation:ExecuteChangeSet",
          "cloudformation:Get*",
          "cloudformation:List*",
          "cloudformation:SetStackPolicy",
          "cloudformation:SignalResource",
          "cloudformation:UpdateStack",
          "cloudformation:ValidateTemplate"
      ],
      "Resource": "*"
    }
  ]
}
```

## Setting up a domain and subdomain in AWS

From Route53 ... 

## VPN and subnets

If you are creating a new account, AWS should create a VPC for you, but if you have an older account you may need to create your own VPC.

Go to the VPC Dashboard and create a VPC. I used `10.0.0.0/16` as the CIDR value.

Next go to the Subnets tab and create two subnets, making sure to choose different availability zones for each one. I used a `10.0.128.0/17` / `10.0.128.0/17` split when creating them.

You will now have values for:

* `VPC_ID`
* `SUBNET_CIDR`
* `SUBNET_ID_A`
* `SUBNET_ID_B`

These values can be inserted into the [`configure_continuum_settings.py
`](https://github.com/elifesciences/elife-continuum-documentation/blob/master/elife-continuum-docs/configure_continuum_settings.py) script for preparing the configuration of the different settings files that are needed to build your environment.


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

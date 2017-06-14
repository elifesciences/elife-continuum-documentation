# Builder setup

Builder is a command line tool for the provisioning and deployment of Continuum component instances.

Refer to [https://github.com/elifesciences/builder] for setting it up. The steps are also documented at [https://github.com/elifesciences/anonymous-formula] which is used to set up AWS EC2 instances running new versions of builder to test it (it's a bit meta).

Your `settings.yml` needs to point to a configuration file forked from `projects/continuum.yaml`. Most of the AWS parameters such as VPC and subnets need to be configured there. Refer to [https://github.com/elifesciences/anonymous-formula/blob/master/salt/anonymous/config/srv-builder-settings.yml] for a sample of `settings.yml` to use.

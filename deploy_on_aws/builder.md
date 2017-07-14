# Builder setup

Builder is a command line tool for the provisioning and deployment of Continuum component instances.

Refer to [https://github.com/elifesciences/builder] for setting it up. The steps are also documented at [https://github.com/elifesciences/anonymous-formula] which is used to set up AWS EC2 instances running new versions of builder to test it (it's a bit meta).

Your `settings.yml` needs to point to a configuration file forked from `projects/continuum.yaml`. Most of the AWS parameters such as VPC and subnets need to be configured there. Refer to [https://github.com/elifesciences/anonymous-formula/blob/master/salt/anonymous/config/srv-builder-settings.yml] for a sample of `settings.yml` to use.

The `projects/continuum.yaml` is configured an eLife test AWS account that you likely won't be able to use. You should make your own copy of this file and modify `settings.yml` to point to it, as the [AWS requirements](requirements.md) will need to be filled in there.

Moreover, you should set `write-*-to-s3` keys in `settings.yml` to `False` as the builder does not support writing backup to a custom S3 bucket yet.

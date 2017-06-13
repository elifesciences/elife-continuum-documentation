# Requirements

## AWS account

Inside your AWS account, you will need:

- your AWS account id, e.g. `501234567890`.
- a VPC along with its id, e.g. `vpc-acdefg12`.
- two publicly routable subnets in two different availability zones, along with their ids and CIDR e.g. `subnet-12345678` and `172.31.0.0/20`, `subnet-90abcdef` and `172.31.48.0/20`.
- (for services using RDS) two additional subnets not publicly routable, which will be used for databases.
- a Route 53 public hosted zone, with a domain such `thedailybugle.org`.
- a Route 53 private hosted zone, with a internal domain such as `thedailybugle.internal`.
- a wildcard SSL certificate, e.g. for `*.thedailybugle.org`; along with its private key and certificate chain in PEM format.

### Known constraints

Only 2nd level domains are supported, such as `thedailybugle.org`. Different components of continuum may expose subdomains of the main one.

Only the `us-east-1` region is supported.

## Github

Along with a Github account, you will need a private key associated to (any) user to automatically clone Git repositories. All repositories are public besides the `builder-private` you will create later containing all credentials; that repository however will be accessed through a deployment key.

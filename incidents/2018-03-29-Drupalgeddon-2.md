# 2018-03-29 - Drupalgeddon II

**Incident Leader: Chris Wilkinson**

## Description

Slow response to highly critical vulnerability.

## Timeline

2018-03-21: announcement from Drupal.org saying to "update within hours" on 2018-03-28 7 PM as automated attacks are expected

2018-03-29 10:30 at standup prioritization happens

2018-03-29 11:02 reading platform.sh blog post and starting mitigation

11:06 [pull request](https://github.com/elifesciences/journal-cms/pull/291) updating journal-cms to 8.4.6

11:15 looking at crm-formula to understand how to upgrade the underlying Drupal, which is unclear

11:26 creating new Civi Vagrant instance
    emailing Luke

11:31 journal-cms is [deployed](https://alfred.elifesciences.org/job/prod-journal-cms/261/console) after test suite runs

11:44 Civi vagrant up breaks due to Python 3 requirement
    mac-requirements.txt breaks with Python 3, hasn't been updated
    reverted local builder to Python 2 to get it working on Mac

11:53 Civi vagrant up tries to grab a database, but it fails due to S3 access
    Unable to create a local version

12:58 crm--ci is there, but not up-to-date and different from production
    highstate, but it starts downloading lots of stuff and fails
    crm-prod is the only up-to-date instance
    back to the formula to understand whether highstate will overwrite any patch: it shouldn't happen

13:23 ssh into crm--prod, remote host identification has changed
    potential hack?
    assumption (correct) is it has been rebuilt

13:32 able to SSH

13:40 patched crm--prod manually
    checking the Civi homepage to check for broken stuff
    trying to audit the machine for signs of hacks

13:48 pinging Graham for proper upgrade

16:06 no knowledge from Graham, Luke is the person for it

2018-04-03: [Jira ticket for Civi Drupal upgrade](https://elifesciences.atlassian.net/browse/CIT-42)

## Contributing Factor(s)

- no awareness of upcoming patch
- no clear update process for `crm` stacks
- builder broken on Mac
- local instances of `crm` cannot be created
- out of hours (even for Luke) critical security release

## Stabilization Steps

- Updating journal-cms to newer version
- Manual patching of crm--prod

## Impact

- 15 hours time window for journal-cms--prod hacking
- 18 hours time window for crm--prod hacking

MTTD: 15 hours
MTTR: 3 hours 10 mins

## Corrective Actions

- Drupal minor release update to 8.5.1 (NATHAN)
- Automated process for continuous update of patch versions of Drupal (NATHAN, GIORGIO)
- Definition of cut-off point for turning off an affected service, as an amendment of playbook (PAUL S)
- Outsourcing of Civi operations, including a staging server (NATHAN)
- Process for receiving security alerts from Drupal (NATHAN)
- Playbook of emergency update of crm--prod (LUKE)
- Python 3 builder should work on Mac (GIORGIO, LUKE)

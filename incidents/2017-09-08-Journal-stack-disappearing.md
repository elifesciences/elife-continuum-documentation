# 2017-09-09 Journal Stack Disappearing

**Incident Leader: Giorgio Sironi**

## Description

Journal prod stack was destroyed preventing https://elifesciences.org existing and was unreachable

## Timeline

16:08 _Stack deletion begins_

16:09 Reported by multiple parties as site failing, not responding

16:10 curl returns no DNS response

16:20 Giorgio checked various apps, dashboard was reachable, it was a journal problem

16:21 _Stack deletion ended_

16:22 Journal stack is noted as missing from EC2 and AWS

16:23 Started creating the stack but without CDN for expediency
      Created DNS on Route 53
      No software running on the servers but requests were being received

16:31 Blank page is seen at https://elifesciences.org

16:40 Homepage is visible (served by 1 server)

16:44 Giorgio disabled credentials that issues delete commands

16:49 IP Address identified as in "Croydon, London"

16:53 Paul contacts Paul M at Digirati

16:59 Digirati confirm was operator/script related and not a hack

17:13 Re-enabled credentials and committed the builder modifications to show we are missing CloudFront CDN

17:17 New Relic showing stats again after server start up issue with its agent (phpFPM was not restarted)

17:28 Deposit confirmation email received signaling bot is re-enabled and confirmed with James G in production team

2017-09-11

09:03 CloudFront CDN recreated and DNS re-pointed

## Contributing Factor(s)

- delete commands should be limited to IT Admin team
- key is shared and assigned to a person (Graham) so not simple to see what/who is issuing the commands
- key has too many permissions, even a production key for Graham doesn't need that level of permissions
- needed Giorgio to bring up the stack
- New Relic late alert, to the wrong email address, and not app focused

## Stabilization Steps

- Re-create journal with builder, without CDN
- disabling the key that performed the delete

## Impact

- no traffic to https://elifesciences.org until recovered
- extended period of production workflow outage (0:30) while credentials were disabled, publishing was delayed

MTTD: 0:01 (0:07 until first alert)

MTTR: 0:32

## Corrective Actions

- Update New Relic to alert to the correct address and test with a dry run of removing a machine (GIORGIO) [ELPP-3148](https://elifesciences.atlassian.net/browse/ELPP-3148)
- Create more fine grain keys and use for bot and development (GIORGIO) [ELPP-3149](https://elifesciences.atlassian.net/browse/ELPP-3149)
- Revoke permissions in existing keys are superfluous (GIORGIO) [ELPP-3149](https://elifesciences.atlassian.net/browse/ELPP-3149)
- Investigate termination protection for production instances (GIORGIO) [ELPP-3149](https://elifesciences.atlassian.net/browse/ELPP-3149)
- Access to console for all tech team staff needs to be enabled (DAVID)
- Playbook for this type of incident (how to create a new stack quickly, and restore a database) (GIORGIO) [Playbook on recreating stacks](https://github.com/elifesciences/continuum-playbook/blob/master/operations/recreating_stacks.md)

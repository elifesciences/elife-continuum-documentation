# 2017-08-25 - Lax backfill service degradation

**Incident Leader: Chris Wilkinson**

## Description

Lax becoming very slow during a backfill and preventing journal from serving article pages.

## Timeline

0:03: backfill is started by Luke

4:15: New Relic alert on recommendations--prod and journal--prod, timing out.

7:48: Chris notices lax--prod is slowing down because of the backfill. Luke is online at this point as well.

Initial thought is recommendations is hammering lax--prod, it was the first backfill after the recommendations stateless change.

8:50: A Journal change can reduce the amount of load on recommendations--prod (and in turn lax--prod). Doesn't deploy because of smoke tests pinging the backends, has to be hotfixed.

Change doesn't make a difference.

9:36: Turning off recommendations--prod nginx, disabling it. Journal copes, serving stale cache copies or hiding it.

10:36: lax--prod has run out of CPU credits, becoming slow. Luke notices.

10:38: without seeing that, Chris turns on recommendations again.

10:52: Luke is "going to try something tricky", lowering the priority of the backfill process. No change.

11:15: Chris is alone on the problem.

11:20: Stealing the screen session on lax--prod. Very long time to completion is estimated.

11:27: trying to stop the backfill.

11:36: backfill process is not running anymore.

11:37: CPU credits on lax--prod started to rise.

11:41: recommendations--prod is turned back on.

11:42: looked in the playbook. Log file of backfill is available, not sure if articles are in a broken state.

11:46: journal--prod error rate is 0.

12:05: journal--prod proper deploy to fix the red build.

## Contributing Factor(s)

- only one EC2 instance
- instance is a `t2.small`, burstable type with CPU credits
- no notification of CPU credit balance being 0
- lack of knowledge about how to stop a backfill
- not all team members on Slack
- not all team members notified of Luke going offline during the incident

## Stabilization Steps

- Turned off recommendations (unsuccessful)
- Stopping the backfill

## Impact

Stale content in journal and potentially broken article pages for ~7 hours.

MTTD: 3:33

MTTR: 3:46

## Corrective Actions

- Make Luke aware that Paul Kelly's report problem may be related to this backfill (SIAN DONE)
- Make everyone aware not to do backfills at the moment (PAUL)
- Make Lax load balanced and run backfill only on one instance https://elifesciences.atlassian.net/browse/ELPP-3026 (GIORGIO)
- Measure times from three backfill phases (generate, validate, ingest) to look for optimizations like [avoiding ingests on unchanged articles](https://elifesciences.atlassian.net/browse/ELPP-3068). To be investigated *after* it is load balanced (GIORGIO)
- Set up some kind of monitoring on CPU credits, possibly New Relic. Ask New Relic contacts (GIORGIO)
- Amend playbook on backfill to include both starting and stopping (GIORGIO)
- Ensure all team members use Slack on incidents (PAUL)

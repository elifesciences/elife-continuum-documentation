# 2017-07-24 - Search unavailable

**Incident Leader: Chris Wilkinson**

## Description

Search service failure led to missing site content and inability of users to perform new searches.

## Timeline

19:03: New Relic email sent notifying of search failure.

20:30: cw checked - no work email; checked New Relic phone app, found it was red for search. Rechecked email; discovered email had been auto deleted due to filters.

Investigation:

Knew backfill had happened earlier in the day, but had done before with no problems.

Knew we'd recently implemented index on demand, checked and found old indices had been kept: 3 old ones of about 600Mb, the current one was 2.6Gb which seemed much too large.

With no experience of Elastic Search had to learn on the fly how to remove old indices.

21:41: Deleted old indices.

22:13: Noticed current index keep growing to fill newly free disk space. Suspected corruption. Deleted index. Search now available, but listing page lists were empty. Initiated reindex.

22:16: Gearman workers died.

22:18 Gearman workers restarted.

22:21: noticed journal homepage had recent content again.

22:24 reindex complete: new index size 1.1Gb.

22:29 confident all search list caches updated. INCIDENT ENDS.

Final index size stable at 558Mb.

## Contributing Factor(s)

- no playbook
- no visual admin tools
- alert email auto-deleted by filter
- search disk was full

## Stabilization Steps

Deleting old indices then reindexing.

## Impact

Home page missing content for ~8 mins.

Maximum possible time listing content might have been empty was 16 mins.

Search service erroring 19:03 - 22:13.

No new (uncached in journal), user searches could be performed for the duration of the incident.

MTTD: 1 hour 27 minutes.

MTTR: 3 hours 26 mins.

## Corrective Actions

Cause still unknown, logs now unavailable.

Share incident report with Digirati. (CHRIS)

Create playbook. (GIORGIO)

Change Lax to emmit update events upon backfill, only of modified articles, rather than the whole lot. Reduces the workload on consuiming services. (LUKE)

Create Timebox ticket to investigate elastichq.org. (DAVID)

Deleting previous index when reindexing has completed. (DONE)

Set up incident response Slack channel. (DONE)


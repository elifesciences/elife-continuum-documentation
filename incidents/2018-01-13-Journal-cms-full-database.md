# 2017-09-09 Journal CMS full database

**Incident Leader: Chris Wilkinson**

## Description

The `journal-cms--prod` stack filled the database space, stopping any interaction with it and read from the API.

## Timeline

03:12 first alerts from New Relic (`journal--prod` and `journal-cms--prod` error percentage high)

05:55 alert journal-cms--prod--1 host not reporting

08:32 Chris cannot log in through SSH, connection hangs

08:36 Chris restarts `journal-cms--prod`

08:41 host restarted and accessible, but database errors such as `SQLSTATE[HY000]: General error: 1205 Lock wait timeout exceeded; try restarting transaction`

08:53 RDS console says `journal-cms--prod`'s database is full

08:55 space usage detected as going down from 60% to 0% between 02:00 and 03:10.

It is later understood that this change was from 60 MB free to 0 MB free.

09:34 elifesciences.org is confirmed as still reachable in random sampled pages, using cached API responses

09:39 the SQS queue of `journa-cms--prod` is identified as still containing messages and correlated with the disk filling. Messages are identified as `elife-metrics` events.

09:41 the cache rebuilds on `journal-cms--prod` are hanging due to the full db, and are manually killed.

09:42 stopping all long-running processes and crons to avoid attempts to write to the database.

09:49 starting increase of db size through Cloud Formation (12 GB to 24 GB)

10:32 Cloud Formation update failed because `The specified database instance is currently in storage-full state. Please allocate more storage by modifying the DB instance.`

10:33 starting increase of db size through RDS console

10:51 space increase completed
      /ping works


## Contributing Factor(s)

- no way to notice database was getting full
- processes hanging which made the EC2 instance crash
- graph of RDS space which had no unit of measure
- unnecessary versioning on journal-cms

## Stabilization Steps

1. Restart the instance
2. Stop all processes like cache rebuild and article import
3. Increase RDS size through console directly

## Impact

Not cached data not available on elifesciences.org, but random sampling shown was not much scope

MTTD: 5h30m from New Relic measurement and alert to first Slack post

MTTR: 7h34m from alert to /ping working again

## Corrective Actions

- alert on RDS space [GIORGIO, LUKE]
- check or update the TTL of journal's caches (API and CloudFront, IIIF). Can we turn off journal-cms for 72 hours and rely on caches? [CHRIS]
- investigation: see if we can turn off revisions for article content (especially views) and clean up old data left there [NATHAN]
- investigation: can we set up autoscaling on RDS space? [GIORGIO]
- investigate: data gathering from New Relic to expose pages there as a dashboard [SEAN]
- extract from logs where processes were hanging so that we can set up a timeout on the db connection [GIORGIO]
- possibly move Drupal’s lock to Redis [CHRIS to clarify]
- logging in recommendations may be insufficient to detect the problem [GIORGIO]

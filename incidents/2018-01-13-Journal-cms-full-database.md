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

09:39 the SQS queue of `journal-cms--prod` is identified as still containing messages and correlated with the disk filling. Messages are identified as `elife-metrics` events.

09:41 the cache rebuilds on `journal-cms--prod` are hanging due to the full db, and are manually killed.

09:42 stopping all long-running processes and crons to avoid attempts to write to the database.

09:49 starting increase of db size through Cloud Formation (12 GB to 24 GB)

10:32 Cloud Formation update failed because `The specified database instance is currently in storage-full state. Please allocate more storage by modifying the DB instance.`

10:33 starting increase of db size through RDS console

10:51 space increase completed
      /ping works


## Contributing Factor(s)

TBD

## Stabilization Steps

TBD

## Impact

TBD

MTTD: TBD

MTTR: TBD

## Corrective Actions

TBD

`If you do a post-mortem, actions are to fix logging in Recommendations and to move Drupal’s lock to Redis. Idea for the DB increase in Journal CMS is to find out if revisioning is turned on, and if so, make sure it’s switched off for external data.`
`Revisioning is annoyingly a requirement for using paragraphs. I would love to kill it. I will revisit that. We need it for covers but should be able to pick and choose when it is used.`

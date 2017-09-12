# 2017-09-06 - Search not indexing some content

**Incident Leader: Chris Wilkinson**

## Description

Search not indexing some articles and possible some other content leads to them not appearing on journal.

## Timeline

13:44: Hannah opens a Jira ticket saying an author has called in that their article wasn't on the homepage.

14:46: Chris is looking at search logs.

Seeing some 404s to Lax, trying running a backfill.

15:10: Cannot run a backfill single. Had to update the XML repository.

15:18: ElasticSearch has logged errors saying that it can't parse the authorResponse. Bunch of errors, not just this article (assuming this one is in the affected set).

15:32: ElasticSearch derives the schema from the content that's being indexed. An Exeter change reflects in a different schema, and search rejects them. We see the body of an article is specially treated to avoid this problem but it's not applied to other parts of articles, and also other content types.

15:56: PR against api-dummy with the new format, to reproduce the error locally in Search's tests.

16:02: PR against search applying the same fix of the body to the authorResponse.

16:17: Search PR merged.

16:24: Deployed in production.

16:26: Reindexing that article.

16:27: Confirmed in the search results.

16:28: Appearing on the homepage.

16:42: All 5 articles we know about are being reindexed.

16:48: Triggering a full reindex.

17:01: Reindexing finished, all articles that could be fixed are visible now.

## Contributing factors

We didn't know Exeter had started changing the input XML in this way (more complex author responses).

We weren't notified that ElasticSearch had failed and in general of the search error log being populated. The error was logged in search application logs but with no article id so no way to find it.

## Stabilization steps

Trying to backfill a single article to reindex it didn't work, no change. But we saw errors being logged which was useful.

Fixed the bug with a change in Search preprocessing the authorResponse.

Reindex single affected articles, than reindex everything to make sure.

## Impact

Subset of articles wouldn't appear in the homepage or in listing or in searches. Most VOR published after Monday were affected.

MTTD: ~72:00 hours (don't exactly know the start of it but was Monday in India)

MTTR: 3:17

## Corrective Actions

- Fix search lack of support for field of content types with complex structure (authorResponse in articles but also other article fields but also other content types) (CHRIS) [ELPP-3153](https://elifesciences.atlassian.net/browse/ELPP-3153)
- We need to be notified when Search logs produces this kind of errors, either through Loggly or New Relic (GIORGIO) [ELPP-3151](https://elifesciences.atlassian.net/browse/ELPP-3151)
- Pipeline that updates kitchen sink should notice their changes, and we should check they are indexed and propagated everywhere (GIORGIO) [ELPP-3152](https://elifesciences.atlassian.net/browse/ELPP-3152)

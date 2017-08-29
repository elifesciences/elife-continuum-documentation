# 2017-08-23 - Journal-cms unpublished articles

**Incident Leader: Chris Wilkinson**

## Description

A large amount of article snippets becoming unpublished on journal-cms, affecting covers and collections linked to them.

## Timeline

13:43: Giuliano discovers some content is missing through its phone

13:52: Emma posts that collections are missing lots of articles

Lots of articles in journal-cms have become unpublished.

They had an updated date of yesterday, 21:16 - the time of the daily update when a new Salt highstate is run (e.g. for security package updates)

Looked at all known logs but not sure of the cause.
- SQS monitoring doesn't show a spike in notifications around that time.
- Monolog long-running process journal-cms logs do not show messages being processed. On 22/8 there are no "Received message" logs after ~16:00.

Manually created a notification for a single article - doesn't fix it, reproduces the problem.

15:01: manually sending notifications while adding error logs to track the bad data coming into journal-cms.

15:30: Giorgio leaves 

15:41: the problem is discovered in how streams are accessed to get the body of the response - once a stream is read further reads return "".

Need to run through all the articles. Decided not to use the Drush `aia` single batch command as it would affect *all* articles.

16:01: updated the articles for the cover items (homepage). `/covers` doesn't start to work so waiting for the cache to expire.

Listing the unpublished article ids so that we can update them by triggering new bus notifications.

16:39: sending notifications for all articles experiencing the problem.

16:56: article notifications finished.

2 articles were leftover, retriggered manually.

Merging pull request with the proper fix, with the intent of clearing the cache with its deploy.

17:13: PR is deployed in production.

Carousel now working, collections and their article content too.

Evening: cause of the bug is a change in the logging that started to log the response body, reading it before it was read by the rest of the code. We still don't know why the articles got updated.

## Contributing Factor(s)

- Wrong method in the PSR library (stream) being used. Many people are using it.
- Lack of error handling (/covers API should use 500, empty response causes the article to become unpublished rather than exception)
- Page cache: /covers didn't recover as quickly as it could

## Stabilization Steps

- Code change through deploy
- Sent notifications manually to recover the correct status for article snippets
- Cleared caches (journal-cms)


## Impact

Carousel missing on homepage for ~3 hours.
Articles in collections missing for at least ~3 hours, up to ~20 hours.

MTTD: 16:28

MTTR: 3:20

## Corrective Actions

- Restore available backups to see the state of the database during the incident (NATHAN, GIORGIO)
- Replace every PSR stream method usage with the correct `__toString()` usage (CHRIS DONE, NATHAN TO REVIEW)
- Make sure error handling on metrics and article updates in journal-cms is adequate (NATHAN, CHRIS TO REVIEW)
- Stop journal-cms from caching while maintaining an acceptable performance (https://elifesciences.atlassian.net/browse/ELPP-2426)
- Introduce a New Relic Synthetics ping check for `/` and `/magazine` (PAUL, CHRIS)

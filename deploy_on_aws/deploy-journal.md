# Deploying journal

`journal` is the Continuum public website, exposing all content to the general public. It relies on an API to separate content from presentation.

Run
```
./bldr deploy:journal,prod
```
to deploy a new `journal--prod` stack (or update an existing one.)

Refer to [https://github.com/elifesciences/builder-private-example/blob/master/pillar/journal.sls] for journal configuration.

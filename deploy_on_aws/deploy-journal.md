# Deploying journal

`journal` is the Continuum public website, exposing all content to the general public. It relies on an API to separate content from presentation.

Run
```
./bldr deploy:journal,baseline
```
to deploy a new `journal--baseline` stack (or update an existing one.)

We are using the `baseline` environment for all stacks, which should correspond to the most basic configuration (excluding additional components such as CDNs or load balancers).

Refer to [https://github.com/elifesciences/builder-private-example/blob/master/pillar/journal.sls] for journal configuration.

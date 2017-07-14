# Deploying api-dummy

`api-dummy` is an helpful project providing a stubbed version of the Continuum API. `journal` can run on top of `api-dummy` for demonstrative purposes, and the project itself is useful for other projects depending on the API to run their tests.

Run
```
./bldr deploy:api-dummy,baseline
```
to deploy a new `api-dummy--baseline` stack (or update an existing one.)

We are using the `baseline` environment for all stacks, which should correspond to the most basic configuration (excluding additional components such as CDNs or load balancers).

Refer to [https://github.com/elifesciences/builder-private-example/blob/master/pillar/api-dummy.sls] for api-dummy configuration.

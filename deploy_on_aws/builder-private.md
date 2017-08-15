# Creating a builder-private repository

A `builder-private` is a private Git repository containing all configuration information about your Continuum instances, including sensitive informations such as passwords, certificates and private keys. A subset of these information will be picked up by the master server for the provisioning of the instances that make up Continuum.

https://github.com/elifesciences/builder-private-example is a sample repository to be filled with your own configuration. You should create a private repository copying the file structure of this repository, and fill in the values. Documentation is provided in the form of README files in the example repository, and with comments in the single configuration files. `builder-private-example` is a reference, not a turnkey solution.

To make sure the `salt/top.sls` file is up-to-date for a particular project, check the corresponding `example.top` file inside the project formula (e.g. https://github.com/elifesciences/journal-formula/blob/master/salt/example.top for `journal`). These top files are tested with the Vagrant VM of each project, and must be kept up-to-date for the provisioning to work here.

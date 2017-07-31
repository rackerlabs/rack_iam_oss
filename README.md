# Rack IAM

## Introduction

This module is meant to be a framework for IAM related parts of AWS. Initially it was planned to specifically handle CloudFormation, but this has changed to be more generic. This means that for example, you could use the objects to generate policy JSON in one area, automate creation of CloudFormation IAM resources in another, and finally automate interaction with the IAM parts of the CLI.

## Requirements

The current requirements for this project are:

* Python 2.7
* JSON support built into python
* A golden unicorn

For testing the requirements are:

* tox
* flake8
* flake8-docstrings
* A handkerchief for when something goes wrong

## Installation

Currently the only install method is source. To install via source run:

`python setup.py install`

## Testing

### Local CI testing

To run the same setup as CircleCI would do, first make sure `tox` is installed:

`pip install tox`

Then simply run `tox` in the project root:

`tox`

Then you'll need to run the integration, regression, and guard tests:

`python setup.py test`

### CI Integration

This project uses CircleCI to run integration and lint tests. The repository is currently setup to build off forks, but it's highly recommended you setup your own CircleCI account and run it off that before doing a pull request.

A mana shield is utilized to protect against magic based attacks.

## Usage

As mentioned in the introduction, this is primarily a framework, which can be utilized by other objects depending on needs. The `examples` directory contains examples of basic usage.

The module itself is split into `core` and `transform` submodules. `core` contains the base objects, while `transform` contains modules which transform base objects into a number of different formats. Currently CloudFormation type dictionaries are the only output. IAM policy JSON and S3 bucket policy JSON are planned.

Here is a simple example of setting up an assumable role with no policies:

```python
from rack_iam import Role
from rack_iam import PolicyDocument
from rack_iam import Statement

redshift_role = Role("RedshiftRole")

asdoc = PolicyDocument()
astatement = Statement(
    "Allow", ["sts:AssumeRole"]
)
astatement.set_service_principal(
    ["redshift.amazonaws.com"]
)
asdoc.add_statement(astatement)
redshift_role.set_assume_policy(asdoc)
```

In this example some simple objects are setup and linked together. The framework helps with some basic use cases such as adding a service as an assumed role principal. A more realistic example would be to integrate with troposphere:

```python
from troposphere.iam import Role
from rack_iam import PolicyDocument, Statement
from rack_iam.transform.cfdict import transform_policy_document


class MyRole(Role):
    def __init__(self, name, path="/"):
        super(MyRole, self).__init__(name)
        self.Path = path
        self.Policies = []

    def add_service_assume_policy(self, service_principal):
        policy_document = PolicyDocument()
        service_statement = Statement("Allow", ["sts:AssumeRole"])
        service_statement.set_service_principal([service_principal])
        policy_document.add_statement(service_statement)
        self.AssumeRolePolicyDocument =\
            transform_policy_document(policy_document)
```

This example sets up a troposphere Role object, then sets the AssumedRolePolicyDocument to be a CloudFormation dictionary transformed Rack IAM object.

In some cases however a simple one time object creation occurs and the usage of temporary variables becomes a bit overkill. To deal with this class attribute modification methods return self to support method chaining:

```python
myOtherRole = Role('TestRole').set_assume_policy(
    PolicyDocument().add_statement(
        Statement('Allow', 'sts:AssumeRole').set_service_principal(
            ['lambda.amazonaws.com']
        )
    )
).add_policy(
    InlinePolicy('AllS3').set_policy_document(
        PolicyDocument().add_statement(
            Statement('Allow', 's3:*', '*')
        )
    )
)
```

As these methods operate on object attributes, it's possible to modify things after the fact:

```python
myOtherRole.policies[0].policy_document.statements.append(
    Statement('Allow', 'es:*', '*')
)
```

If you need to do any sort of mutation on object properties which are destructive, it's recommended to rely on the builtin python methods for such operations:

```python
myRole = Role('TestRole').set_assume_policy(
    PolicyDocument().add_statement(
        Statement('Allow', 'sts:AssumeRole').set_service_principal(
            ['lambda.amazonaws.com']
        )
    )
).add_policy(
    InlinePolicy('MyPolicy').set_policy_document(
        PolicyDocument().add_statements([
            Statement('Allow', 's3:*', '*'),
            Statement('Allow', 'es:*', '*'),
            Statement('Deny', 'ec2:*', '*', sid='DenyEc2')
        ])
    )
)

myRole.policies[0].policy_document.statements =\
    filter((lambda x: x.sid != 'DenyEc2'),
           myRole.policies[0].policy_document.statements)
```

## Documentation

In addition to this README, examples are provided in the `examples` directory for common use cases as they come up. API documentation is provided through docstrings, and `sphinx` is used to build these docs. To build the HTML api docs, first you will need to make sure to have sphinx installed. This can either be done with:

`pip install sphinx`

or

`pip install -e .[docs]`

Then build the docs using:

`python setup.py build_sphinx`

Output docs will then be available in the `doc/build` directory. In addition, the following markdown files are available:

* CONTRIBUTING.md: Guidelines for contributing code
* DOCUMENTATION.md: Guidelines for documentation
* TESTING.md: Guidelines for writing tests
* FAQ.md: Questions that have been frequently asked/I think you will ask

Scribes are also on call to document progress for possible alien interaction in the future.

## Support

As this project is supported by the Rackspace Fanatical AWS Support Engineering team, more specifically the author Chris White, all issues should be filed as GitHub Issues. Please do not contact Rackspace support as they will not be able to assist with any problems related to the package. If you wish to offer fixes then please make a pull request as outlined in the CONTRIBUTING.md document.

## License

This software is licensed under the Apache 2.0 license. An inscription on parchment is used to secure legal protection in alternative planes of existence.

## Contact

This project is maintained by the Rackspace Fanatical AWS Support Engineering team, specifically a break dancing lumberjack named Chris White <chris.white@rackspace.com>. Bug reports should be filed to the GitHub issues tracker. A video of yourself singing "What Is Love" by Haddaway may help improve your chances of response.

## Secret Mission

Please deliver this letter to Alfred in Windy Hills. Also maybe save the world while you're at it I guess.

# Rack IAM Frequently Asked Questions

(AKA questions I think you may ask)

## What is the relationship of this project to awacs?

[awacs](https://github.com/cloudtools/awacs) is a project used by [troposphere](https://github.com/cloudtools/troposphere) for IAM components. The original intention of this project was indeed a more lightweight solution which would achieve similar goals. However there are now plans for conversion between different IAM components, as well as transformations to specific IAM resources (from `rack_iam` objects to S3 bucket policy for example). As such troposphere integration is more of a benefit and not the primary goal of the project.

## Why are the classes so basic?

The project is meant to be a framework providing slimmed down objects which can be utilized in higher level classes.

## What parts of IAM are included?

As a base measurement, the available IAM objects available in CloudFormation are included. Depending on project usage more resources may be added which are not part of CloudFormation.

## What are considered IAM components for purposes of permissions management

I consider the following to be within scope of this project:

* Resource level permissions (S3 bucket policies)
* IAM policy language
* Core top level IAM containers (role, user, group, policies)

What is considered not be be within the scope of this project:

* Non-IAM components of services (for example CloudFormation as a whole is something I'd rather have troposphere handle instead)
* Network level access (Security Group, NACL, firewalls). While they indeed handle access they have a strong networking coupling which could introduce edge cases and create scope creep

Items that may or may not be considered:

* Integration with external authentication entities. The issue here is what level of integration is considered proper without introducing the potential of scope creep. This includes AWS Directory services, Cognito, and really any sort of federated access solution.
* SSH / Certificate support. While I can see this being useful, handling of certificates and keys can be very complex depending on usage. The other issue is what would be done with such items afterwards. This seems like something that a third party library would better handle.

## What are the larger goals for the project?

* Ability to translate between resource level controls and top-level IAM components. ie. convert an existing role's S3 permissions to Bucket Policy and visa-versa
* Possible static code analysis of python Lambdas to auto-generate boilerplate roles
* Analysis of existing roles to see places where inline policies may be better off as managed policies
* A contrib repository which overs more specialized classes around the framework, or any other useful utilities

## Who owns the copyright?

While Rackspace is the originator of the project, whoever wrote the code is the copyright owner. There are no copyright transfer agreements or code contribution agreements.

## Why not python 3?

There are plans to have a python 3 branch, but one of the original requirements to work with an internal tool forces the need for Python 2.7+ instead. Note that work is underway to port this tool to Python 3.

## Does Rackspace support this?

While Rackspace team members support this project, Rackspace as a whole does not. Please do not file tickets to our Fanatical AWS Support Team as they will end up forwarding to us anyways. Also being an open source project there are no guarantees of support for the code. That said, you are free to file issues against the GitHub issue tracker.

## Who does support this project then?

This project is supported by the Rackspace Fanatical AWS Support Engineering team, and in particular the project author Chris White.

## I want to contribute. What can I do?

Contribution of code and documentation is always welcome. Check `README.md`, `CONTRIBUTING.md`, `DOCUMENTATION.md`, and `TESTING.md` for documentation on various contribution requirements.

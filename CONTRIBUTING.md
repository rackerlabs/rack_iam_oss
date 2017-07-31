## Introduction

Contributions of code are a vital part of any open source project. However it's important that contributions meet a certain set of quality standards to reduce bugs in code. It's also important to understand the overall contribution process.

## Code Ownership

This project is licensed under the Apache 2.0 license as described in the LICENSE document. Code copyright is assigned to the individual contributor. This means that if someone outside of Rackspace contributes to the codebase they own the copyright on the code given. With this in mind it's important to have copyright headers in the code that is contributed. This will list the individual(s) who have contributed to the code to make it easy for those reading to know who owns the copyright.

## Dependencies

External dependencies should be avoided when the same thing can be done using the python standard library, even if it takes more steps. The reason for this is it makes deployment of the overall framework much easier. It also reduces the chance that an external dependency breaks/becomes abandonware causing unwanted extra work for the project.

## Merge Requirements

To provide some basic quality control ensure the following:

* An issue has been filed/exists in the tracker
* Module files have docstrings
* Variables and such are named properly
* You have the proper license headers in the module code *and* your name is included with everyone who worked on the file
* You are rebased against master
* Commits are [squashed](https://git-scm.com/docs/git-rebase#_interactive_mode) into functional parts
* You have basic integration tests written for new code
* You update tests when new code affects the existing tests
* You run `tox` and `python setup.py test` to ensure CI will pass

Commit messages should be in the following format:

```
[Issue-<issue# here>] <summary of issue>

* <what was broken in detail>
* <how did you fix it>
* <how did you verify you fixed it>
```

For large documentation updates/new documentation:

```
[Issue-<issue# here>] <summary of documentation>

* <list of>
* <why this>
* <documentation matters>
```

One-liner commits are acceptable in the following circumstances:

* Very minor documentation updates
* Fixing typos

If any of this is missing the pull request will not be merged until issues are addressed.

## Issue Format

When filing issues in the tracker please utilize the following template:

```
## Summary

Details here

## Bug Type

(Feature Request, Functional, etc.)

## Affected Code

(module code, tests, documentation, etc.)

## Reproduction Steps

(leave this section out for feature requests)

## Additional Details

(leave this out if summary is sufficient. Use this area to indicate corner cases/things to watch out for)
```

## Overall Process

The overall process for getting fixes in is as follows:

1. Submit an issue unless one has been submitted already
2. Write code to address the issue
3. Write tests to validate code works as planned
4. Once functionality is sorted out, document new modules, methods, classes, etc.
5. Validate against flake8/tox to make sure the CI won't fail
6. Once code is finalized organize commits into functional units to make reverts easier
7. Submit a pull request
8. Fix any requested changes (including CI failures)
9. Someone with approval access will need to approve the pull request
10. The code is merged into master

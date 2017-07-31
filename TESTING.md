# Rack IAM Testing

While testing is considered somewhat of a duplication of code, it is necessary for this project to ensure some level of stability. In order to reduce external dependencies Rack IAM utilizes the unittest standard library module. This also allows for easy integration with setup tools as well as automated CI with CircleCI. CircleCI runs these tests as well as flake8 (with docstrings) tests.

## Types of Tests

There are three main types of tests utilized:

### Integration Tests

This tests a class or combination of classes in what would be expected usage. Currently these are preferred over testing all possible function combinations via unit tests. In general integration tests look over the following:

* Testing the basic structure of the resulting class
* Verifying certain types when applicable
* For transformation/import classes structure of the output object should be tested against basic usage

### Guard Tests

These tests are meant for testing against either critical components (Generation of ARN values) or one off cases where user input may have different code paths depending on input ( for example if you attempt to add a duplicate username to a group which already contains it ). These should test the special case.

### Regression Tests

If a piece of code committed breaks existing code expectations resulting in a bug, a regression test must be written. This test ensure that the same bug does not occur again.

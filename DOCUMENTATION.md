# Rack IAM Documentation

In order to make this package as easy to use as possible documentation in different forms is provided. These include:

* The main `README.md` file which gives an overview of the project
* The `examples/` directory containing example code to showcase potential common uses
* The `doc/` directory, which will be expanded to explain more complex concepts as the project evolves
* Docstrings in the code. These are converted to HTML using Sphinx

Note that anything in the `rack_iam` directory **must** be documented. CircleCI utilizes `tox` (which in turn leans on `flake8` with the docstrings plugin included) for the test suite. If these fails contributed code will not be merged.

## License

On top of this code also includes license headers for the Apache 2.0 license. These must be preserved, and contributors (who are thus copyright holders) properly noted. Please note that contributions **must** contain the license header.

## Docstrings

Docstrings use the [Google python docstring format](http://google.github.io/styleguide/pyguide.html?showone=Comments#Comments). In addition tox tests the following main docstring conditions (along with some others that I've not hit yet):

* First line of the docstring must end with a period
* Must be in an imperative form (Creates, Removes, Adds)
* There must be a blank line if a Return section is declared

An example of a docstring for a method is:

```
    def add_users(self, users):
        """Add users to policy.

        This adds a list of users to the policy. Ignores duplicate entries as
        well.

        Args:
            users ([]str): The users to add to the policy
        """
        self.users.update(users)
```

Note that you *may* ignore docstrings for unit tests. However it is recommended that you still comment any complex code for those reading it.

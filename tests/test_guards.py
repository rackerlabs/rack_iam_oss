# -*- coding: utf-8 -*-
# Copyright 2017 Rackspace US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
from rack_iam import User
from rack_iam import Group
from rack_iam import Statement
from rack_iam import Policy, ManagedPolicy, InlinePolicy, PolicyDocument
from rack_iam import InstanceProfile, Role
from rack_iam.transform.cfdict.statement import transform_statement


# Guard tests are the testing of edge cases which may happen infrequently
# but when they do we want to ensure that things are working properly. Examples
# of this include adding a username to a group when the username already exists
class GuardTest(unittest.TestCase):
    # This is testing the case of duplicate entries properly being ignored by
    # using sets for various properties. It checks both that the entries are
    # the same even after duplication of the value and that the length of the
    # set is proper
    def test_duplicate_entries(self):
        test_user = User('TestUser', ['group1', 'group2'])
        test_user.add_to_group('group2')
        self.assertTrue(test_user.groups & {'group1', 'group2'})
        self.assertEquals(len(test_user.groups), 2)

        test_group = Group('TestGroup', ['user1', 'user2'])
        self.assertTrue(test_group.users & {'user1', 'user2'})
        self.assertEquals(len(test_group.users), 2)

        test_policy = Policy('TestPolicy', ['group1', 'group2'], ['role1',
                             'role2'], ['user1', 'user2'])
        test_policy.add_users(['user2'])
        test_policy.add_groups(['group2'])
        test_policy.add_roles(['role2'])

        for prop_name in ['group', 'role', 'user']:
            self.assertTrue(test_policy.__dict__['{}s'.format(prop_name)] &
                            {'{}1'.format(prop_name), '{}2'.format(prop_name)})
            self.assertEquals(
                len(test_policy.__dict__['{}s'.format(prop_name)]), 2)

    # Verify that PolicyDocument can add multiple statements
    def test_multiple_statements(self):
        test_policy_doc = PolicyDocument().add_statements([
            Statement('Allow', 's3:*', '*'),
            Statement('Allow', 'ec2:*', '*'),
            Statement('Allow', 'es:*', '*')
        ])
        self.assertEquals(len(test_policy_doc.statements), 3)
        for statement in test_policy_doc.statements:
            self.assertIsInstance(statement, Statement)

    # This tests to see if the ARNs generated for various resources meet the
    # format defined in:
    #
    # http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html
    def test_arns(self):
        self.assertEquals(
            User('TestUser').get_arn(),
            'arn:aws:iam:::user/TestUser'
        )
        self.assertEquals(
            Group('TestGroup').get_arn(),
            'arn:aws:iam:::group/TestGroup'
        )
        self.assertEquals(
            ManagedPolicy('TestManagedPolicy', 'My Managed Policy').get_arn(),
            'arn:aws:iam:::policy/TestManagedPolicy'
        )
        self.assertEquals(
            Role('TestRole').get_arn(),
            'arn:aws:iam:::role/TestRole'
        )
        self.assertEquals(
            InstanceProfile('TestInstanceProfile', 'MyRole').get_arn(),
            'arn:aws:iam:::instance-profile/TestInstanceProfile'
        )

    # Seeing if method chaining works properly
    def test_chaining(self):
        test_user = User('TestUser').set_login_profile('mypass'). \
            set_managed_policy_arns(['arn1', 'arn2'])
        test_group = Group('TestGroup').add_policy(
            InlinePolicy('MyPolicy').set_policy_document(
                PolicyDocument().add_statement(
                    Statement('Allow', 's3:*', '*')
                )
            )
        )
        test_role = Role('TestRole').add_policy(
            InlinePolicy('MyPolicy').set_policy_document(
                PolicyDocument().add_statement(
                    Statement('Allow', 's3:*', '*')
                )
            )
        )
        self.assertIsInstance(test_user, User)
        self.assertIsInstance(test_group, Group)
        self.assertIsInstance(test_role, Role)

    # Validate that statement ID works
    def test_sid(self):
        test_statement = Statement('Allow', 's3:*', sid='Statement123456')
        self.assertEquals(test_statement.sid, 'Statement123456')
        test_dict = transform_statement(test_statement)
        self.assertEquals(test_dict['Sid'], 'Statement123456')

if __name__ == '__main__':
    unittest.main()

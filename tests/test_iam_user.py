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
from rack_iam import User, InlinePolicy, PolicyDocument
from rack_iam import Statement


class EmptyUser(unittest.TestCase):
    def setUp(self):
        self.test_user = User('TestUser')

    def test_basic_structure(self):
        self.assertEqual(self.test_user.username, 'TestUser')
        self.assertEquals(len(self.test_user.policies), 0)
        self.assertEquals(len(self.test_user.managed_policy_arns), 0)
        self.assertIsNone(self.test_user.login_profile)
        self.assertEqual(len(self.test_user.groups), 0)


class BasicUser(unittest.TestCase):
    def setUp(self):
        test_user = User('TestUser', ['group1', 'group2'])

        allpolicydoc = PolicyDocument()
        allstatement = Statement("Allow", ["*"], "*")
        allpolicydoc.add_statement(allstatement)
        allinlinepolicy = InlinePolicy('TestPolicy')
        allinlinepolicy.set_policy_document(allpolicydoc)

        test_user.add_policy(allinlinepolicy)
        test_user.set_managed_policy_arns(['arn1', 'arn2'])
        test_user.set_login_profile('mypass')

        self.test_user = test_user

    def test_basic_structure(self):
        self.assertEqual(self.test_user.username, 'TestUser')
        self.assertEqual(self.test_user.groups, set(['group1', 'group2']))
        self.assertEquals(self.test_user.managed_policy_arns, ['arn1', 'arn2'])
        self.assertEquals(self.test_user.login_profile, ('mypass', True))

    def test_user_policy(self):
        self.assertIsInstance(self.test_user.policies[0], InlinePolicy)

        policy_document = self.test_user.policies[0].policy_document
        self.assertIsInstance(policy_document, PolicyDocument)
        self.assertIsInstance(policy_document.statements, list)

        statement =\
            self.test_user.policies[0].policy_document.statements[0]

        self.assertEqual(statement.effect, "Allow")
        self.assertEqual(statement.action, "*")
        self.assertEqual(statement.resource, "*")


if __name__ == '__main__':
    unittest.main()

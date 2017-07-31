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
from rack_iam import PolicyDocument, InlinePolicy
from rack_iam import Statement
from rack_iam.transform.cfdict import transform_user


class CFBlankUser(unittest.TestCase):
    def setUp(self):
        test_user = User('TestUser')
        self.test_dict = transform_user(test_user)

    def test_structure(self):
        self.assertFalse(
            'Policies' in
            self.test_dict['TestUser']['Properties'])
        self.assertEquals(self.test_dict['TestUser']['Properties']['UserName'],
                          'TestUser')


class CFBasicIamUser(unittest.TestCase):
    def setUp(self):
        test_user = User('TestUser', groups=['group1', 'group2'])

        allpolicy = InlinePolicy('TestPolicy')
        allpolicydoc = PolicyDocument()
        allstatement = Statement("Allow", ["*"], "*")
        allpolicydoc.add_statement(allstatement)
        allpolicy.set_policy_document(allpolicydoc)

        test_user.add_policy(allpolicy)
        test_user.set_login_profile('mypass')
        test_user.set_managed_policy_arns(['arn1', 'arn2'])
        self.test_dict = transform_user(test_user)

    def test_basic_user_structure(self):
        self.assertEquals(
            self.test_dict['TestUser']['Properties']['UserName'],
            'TestUser')
        self.assertTrue('Policies' in self.test_dict['TestUser']['Properties'])
        self.assertTrue('PolicyDocument' in
                        self.test_dict['TestUser']['Properties']['Policies'][0])
        self.assertTrue(
            "Version" in
            self.test_dict['TestUser']['Properties']
            ['Policies'][0]['PolicyDocument'])
        self.assertEquals(
            self.test_dict['TestUser']['Properties']['Groups'],
            set(['group1', 'group2'])
        )
        self.assertEquals(
            self.test_dict['TestUser']['Properties']['ManagedPolicyArns'],
            ['arn1', 'arn2']
        )
        self.assertEquals(self.test_dict['TestUser']['Properties']
                          ['LoginProfile']['Password'], 'mypass')
        self.assertEquals(self.test_dict['TestUser']['Properties']
                          ['LoginProfile']['PasswordResetRequired'], True)

    def test_policy_statement(self):
        statement = (self.test_dict['TestUser']['Properties']['Policies'][0]
                     ['PolicyDocument']['Statement'][0])

        self.assertEqual(statement["Effect"], "Allow")
        self.assertEqual(statement["Action"], "*")
        self.assertEqual(statement["Resource"], "*")


if __name__ == '__main__':
    unittest.main()

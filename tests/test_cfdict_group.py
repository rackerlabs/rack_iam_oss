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
from rack_iam import Group, InlinePolicy, Statement, PolicyDocument
from rack_iam.transform.cfdict import transform_group, transform_group_users


class CFBlankGroup(unittest.TestCase):
    def setUp(self):
        test_group = Group('TestGroup')
        self.test_dict = transform_group(test_group)

    def test_structure(self):
        self.assertFalse(
            'Users' in
            self.test_dict['TestGroup']['Properties'])
        self.assertEquals(self.test_dict['TestGroup']['Properties']
                          ['GroupName'], 'TestGroup')


class CFBasicIamGroup(unittest.TestCase):
    def setUp(self):
        test_group = Group('TestGroup', users=['user1', 'user2'])

        allpolicy = InlinePolicy('TestPolicy')
        allpolicydoc = PolicyDocument()
        allstatement = Statement("Allow", ["*"], "*")
        allpolicydoc.add_statement(allstatement)
        allpolicy.set_policy_document(allpolicydoc)

        test_group.add_policy(allpolicy)
        test_group.set_managed_policy_arns(['arn1', 'arn2'])
        self.test_dict = transform_group(test_group)
        self.test_mapping = transform_group_users(test_group)

    def test_basic_group_structure(self):
        self.assertEquals(
            self.test_dict['TestGroup']['Properties']['GroupName'],
            'TestGroup')
        self.assertTrue('Policies' in self.test_dict['TestGroup']['Properties'])
        self.assertTrue('PolicyDocument' in
                        self.test_dict['TestGroup']['Properties']['Policies'][0])
        self.assertTrue(
            "Version" in
            self.test_dict['TestGroup']['Properties']
            ['Policies'][0]['PolicyDocument'])
        self.assertEquals(
            self.test_dict['TestGroup']['Properties']['Users'],
            set(['user1', 'user2'])
        )
        self.assertEquals(
            self.test_dict['TestGroup']['Properties']['ManagedPolicyArns'],
            ['arn1', 'arn2']
        )

    def test_policy_statement(self):
        statement = (self.test_dict['TestGroup']['Properties']['Policies'][0]
                     ['PolicyDocument']['Statement'][0])

        self.assertEqual(statement["Effect"], "Allow")
        self.assertEqual(statement["Action"], "*")
        self.assertEqual(statement["Resource"], "*")

    def test_user_group_mapping(self):
        self.assertTrue('TestGroupUserAssociation' in self.test_mapping)
        properties = self.test_mapping['TestGroupUserAssociation']['Properties']

        self.assertEquals(properties['GroupName'], 'TestGroup')
        self.assertEquals(properties['Users'], set(['user1', 'user2']))


if __name__ == '__main__':
    unittest.main()

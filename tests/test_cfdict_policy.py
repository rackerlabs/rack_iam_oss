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
from rack_iam import Policy, ManagedPolicy
from rack_iam import PolicyDocument
from rack_iam import Statement
from rack_iam.transform.cfdict import (transform_policy,
                                       transform_managed_policy)


class CFNoPermisionsPolicy(unittest.TestCase):
    def setUp(self):
        test_policy = Policy('TestPolicy')
        self.test_dict = transform_policy(test_policy)

    def test_no_policies(self):
        self.assertFalse(
            'PolicyDocument' in
            self.test_dict['TestPolicy']['Properties'])


class CFBasicIamPolicy(unittest.TestCase):
    def setUp(self):
        test_policy = Policy(
            'TestPolicy',
            groups=['group1', 'group2'],
            users=['user1', 'user2'],
            roles=['role1', 'role2'])
        allpolicydoc = PolicyDocument(policy_id='Policy123456')
        allstatement = Statement("Allow", ["*"], "*")
        allpolicydoc.add_statement(allstatement)
        test_policy.set_policy_document(allpolicydoc)

        self.test_dict = transform_policy(test_policy)

    def test_basic_policy_structure(self):
        self.assertEquals(
            self.test_dict['TestPolicy']['Properties']['PolicyName'],
            'TestPolicy')
        self.assertTrue('TestPolicy' in self.test_dict)
        self.assertTrue('PolicyDocument' in
                        self.test_dict['TestPolicy']['Properties'])
        self.assertTrue(
            "Version" in
            self.test_dict['TestPolicy']['Properties']['PolicyDocument'])
        self.assertEquals(
            self.test_dict['TestPolicy']['Properties']['PolicyDocument']['Id'],
            'Policy123456')
        self.assertTrue(
            self.test_dict['TestPolicy']['Properties']['Users'] &
            {'user1', 'user2'}
        )
        self.assertTrue(
            self.test_dict['TestPolicy']['Properties']['Groups'] &
            {'group1', 'group2'}
        )
        self.assertTrue(
            self.test_dict['TestPolicy']['Properties']['Roles'] &
            {'role1', 'role2'}
        )

    def test_policy_statement(self):
        statement = (self.test_dict['TestPolicy']['Properties']
                     ['PolicyDocument']['Statement'][0])

        self.assertEqual(statement["Effect"], "Allow")
        self.assertEqual(statement["Action"], "*")
        self.assertEqual(statement["Resource"], "*")


class CFBasicManagedPolicy(unittest.TestCase):
    def setUp(self):
        test_managed_policy = ManagedPolicy('TestManagedPolicy',
                                            'A managed policy')

        self.test_dict = transform_managed_policy(test_managed_policy)

    def test_basic_structure(self):
        self.assertTrue('TestManagedPolicy' in self.test_dict)
        self.assertEquals(
            self.test_dict['TestManagedPolicy']['Properties']
            ['ManagedPolicyName'], 'TestManagedPolicy')
        self.assertEquals(
            self.test_dict['TestManagedPolicy']['Properties']
            ['Description'], 'A managed policy')


if __name__ == '__main__':
    unittest.main()

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
from rack_iam import Policy, ManagedPolicy, PolicyDocument
from rack_iam import Statement


class EmptyPolicy(unittest.TestCase):
    def setUp(self):
        self.test_policy = Policy('TestPolicy')

    def test_basic_structure(self):
        self.assertEqual(self.test_policy.name, 'TestPolicy')
        self.assertIsNone(self.test_policy.policy_document)
        self.assertEqual(len(self.test_policy.groups), 0)
        self.assertEqual(len(self.test_policy.users), 0)
        self.assertEqual(len(self.test_policy.roles), 0)


class BasicPolicy(unittest.TestCase):
    def setUp(self):
        test_policy = Policy('TestPolicy')

        allpolicydoc = PolicyDocument(policy_id='Policy123456')
        allstatement = Statement("Allow", ["*"], "*")
        allpolicydoc.add_statement(allstatement)

        test_policy.set_policy_document(allpolicydoc)

        self.test_policy = test_policy

    def test_basic_structure(self):
        self.assertEqual(self.test_policy.name, 'TestPolicy')
        self.assertIsInstance(self.test_policy.policy_document, PolicyDocument)
        self.assertEqual(len(self.test_policy.groups), 0)
        self.assertEqual(len(self.test_policy.users), 0)
        self.assertEqual(len(self.test_policy.roles), 0)

        policy_document = self.test_policy.policy_document
        self.assertIsInstance(policy_document.statements, list)
        self.assertEquals(policy_document.policy_id, 'Policy123456')

    def test_policy_statement(self):
        statement =\
            self.test_policy.policy_document.statements[0]

        self.assertEqual(statement.effect, "Allow")
        self.assertEqual(statement.action, "*")
        self.assertEqual(statement.resource, "*")


class BasicManagedPolicy(unittest.TestCase):
    def setUp(self):
        self.test_managed_policy = ManagedPolicy('TestManagedPolicy',
                                                 'A sample managed policy')

    def test_basic_structure(self):
        self.assertEqual(self.test_managed_policy.name, 'TestManagedPolicy')
        self.assertEqual(self.test_managed_policy.description,
                         'A sample managed policy')

if __name__ == '__main__':
    unittest.main()

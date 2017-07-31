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
from rack_iam import Role
from rack_iam import InlinePolicy, PolicyDocument
from rack_iam import Statement


# A common pattern is to have a role which allows
# a service to assume a role, but doesn't have any
# permissions. For example a Redshift role with
# no permissions, which someone could say allow
# S3 access later when they need it
class ServiceNoPermissionsRole(unittest.TestCase):
    def setUp(self):
        test_role = Role("BlankRole")

        asdoc = PolicyDocument()
        astatement = Statement(
            "Allow", ["sts:AssumeRole"]
        )
        astatement.set_service_principal(
            ["ec2.amazonaws.com"]
        )
        asdoc.add_statement(astatement)
        test_role.set_assume_policy(asdoc)

        self.test_role = test_role

    def test_no_policies(self):
        self.assertEqual(len(self.test_role.policies), 0)

    def test_assume_role_policy_document_present(self):
        self.assertIsInstance(
            self.test_role.assume_role_policy_document, PolicyDocument)


class BasicIamRole(unittest.TestCase):
    def setUp(self):
        test_role = Role("RootRole")

        adoc = PolicyDocument()
        astatement = Statement(
            "Allow", ["sts:AssumeRole"])
        astatement.set_service_principal(
            ["ec2.amazonaws.com"])
        adoc.add_statement(astatement)

        allpolicy = InlinePolicy("root")
        allpolicydoc = PolicyDocument()
        allstatement = Statement("Allow", ["*"], "*")
        allpolicydoc.add_statement(allstatement)
        allpolicy.set_policy_document(allpolicydoc)

        test_role.set_assume_policy(adoc)
        test_role.add_policy(allpolicy)

        self.test_role = test_role

    def test_basic_role_structure(self):
        self.assertEqual(self.test_role.name, "RootRole")
        self.assertIsInstance(self.test_role.assume_role_policy_document,
                              PolicyDocument)
        self.assertIsInstance(self.test_role.policies, list)
        self.assertIsInstance(self.test_role.policies[0], InlinePolicy)

    def test_role_assume_policy_document(self):
        assume_policy = self.test_role.assume_role_policy_document

        self.assertIsInstance(
            assume_policy.statements, list)

        self.assertEqual(
            len(assume_policy.statements), 1)

        statement = assume_policy.statements[0]

        self.assertEqual(
            statement.effect, "Allow")

        self.assertIsInstance(statement.action, list)

        self.assertEqual(
            statement.action, ["sts:AssumeRole"])

    def test_role_policy(self):
        policies = self.test_role.policies

        self.assertIsInstance(policies, list)
        self.assertIsInstance(policies[0], InlinePolicy)

        policy = policies[0]
        self.assertEqual(policy.name, "root")
        self.assertIsInstance(policy.policy_document, PolicyDocument)

        policy_document = policy.policy_document
        self.assertIsInstance(policy_document.statements, list)

    def test_policy_statement(self):
        statement = self.test_role.policies[0].policy_document.statements[0]

        self.assertEqual(statement.effect, "Allow")
        self.assertEqual(statement.action, "*")
        self.assertEqual(statement.resource, "*")

if __name__ == '__main__':
    unittest.main()

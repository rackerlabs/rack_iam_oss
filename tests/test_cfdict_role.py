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
from rack_iam.transform.cfdict import transform_role


# A common pattern is to have a role which allows
# a service to assume a role, but doesn't have any
# permissions. For example a Redshift role with
# no permissions, which someone could say allow
# S3 access later when they need it
class CFServiceNoPermissionsRole(unittest.TestCase):
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

        self.test_dict = transform_role(test_role)

    def test_no_policies(self):
        self.assertFalse(
            "Policies" in
            self.test_dict["BlankRole"]["Properties"])

    def test_assume_role_policy_document_present(self):
        self.assertTrue(
            "AssumeRolePolicyDocument" in
            self.test_dict["BlankRole"]["Properties"]
        )


class CFBasicIamRole(unittest.TestCase):
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

        self.test_dict = transform_role(test_role)

    def test_basic_role_structure(self):
        self.assertTrue("RootRole" in self.test_dict)
        self.assertTrue(
            "AssumeRolePolicyDocument" in
            self.test_dict["RootRole"]["Properties"]
        )
        self.assertIsInstance(
            self.test_dict["RootRole"]["Properties"]["Policies"], list)
        self.assertTrue(
            "Version" in
            self.test_dict["RootRole"]["Properties"]
            ["Policies"][0]["PolicyDocument"])

    def test_role_assume_policy_document(self):
        assume_policy = (self.test_dict["RootRole"]["Properties"]
                         ["AssumeRolePolicyDocument"])

        self.assertIsInstance(
            assume_policy["Statement"], list)

        self.assertEqual(
            len(assume_policy["Statement"]), 1)

        statement = assume_policy["Statement"][0]

        self.assertEqual(statement["Effect"], "Allow")

        self.assertIsInstance(statement["Action"], list)

        self.assertEqual(
            statement["Action"], ["sts:AssumeRole"])

    def test_role_policy(self):
        policies = self.test_dict["RootRole"]["Properties"]["Policies"]

        self.assertIsInstance(policies, list)
        self.assertTrue("Version" in policies[0]["PolicyDocument"])

        policy = policies[0]
        self.assertEqual(policy["PolicyName"], "root")
        self.assertTrue(policy["PolicyDocument"])

        policy_document = policy["PolicyDocument"]
        self.assertIsInstance(policy_document["Statement"], list)

    def test_policy_statement(self):
        statement = (self.test_dict["RootRole"]["Properties"]
                     ["Policies"][0]["PolicyDocument"]["Statement"][0])

        self.assertEqual(statement["Effect"], "Allow")
        self.assertEqual(statement["Action"], "*")
        self.assertEqual(statement["Resource"], "*")

if __name__ == '__main__':
    unittest.main()

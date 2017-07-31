# This example uses Rack IAM along with Troposphere to generate a
# Cross account role that can be assumed for S3 access
from troposphere.iam import Role, Policy
from troposphere import Template, Parameter, Ref, Join, GetAtt, Output
from rack_iam import PolicyDocument, Statement
# This transformation generates a python dictionary which mocks what
# a cloud formation JSON object would look like. For the case of IAM,
# troposphere can accept these as property values for certain types.
from rack_iam.transform.cfdict import transform_policy_document


# This is an example of an abstraction around the Rack IAM framework.
# A number of basic use cases are covered here.
class MyRole(Role):
    def __init__(self, name, path="/"):
        super(MyRole, self).__init__(name)
        self.Path = path
        self.Policies = []

    def add_service_assume_policy(self, service_principal):
        policy_document = PolicyDocument()
        service_statement = Statement("Allow", ["sts:AssumeRole"])
        service_statement.set_service_principal([service_principal])
        policy_document.add_statement(service_statement)
        # An example of using a transform to make the Rack IAM
        # objects usable by Troposphere
        self.AssumeRolePolicyDocument =\
            transform_policy_document(policy_document)

    def add_account_assume_policy(self, account_id, external_id=None):
        policy_document = PolicyDocument()
        account_statement = Statement("Allow", ["sts:AssumeRole"])
        account_statement.set_account_principal(
            account_id, external_id=external_id)
        policy_document.add_statement(account_statement)
        self.AssumeRolePolicyDocument = \
            transform_policy_document(policy_document)

    def add_policy(self, policy_name, effect, action="*", resource="*"):
        # Troposphere object
        policy = Policy(title=policy_name)
        policy.PolicyName = policy_name

        policy_document = PolicyDocument()
        statement = Statement(effect, action, resource=resource)
        policy_document.add_statement(statement)

        policy.PolicyDocument = transform_policy_document(policy_document)
        self.Policies.append(policy)

    def add_multi_statement_policy(self, policy_name, statements):
        # Troposphere object
        policy = Policy(title=policy_name)
        policy.PolicyName = policy_name

        policy_document = PolicyDocument()
        for statement in statements:
            policy_document.add_statement(statement)

        policy.PolicyDocument = transform_policy_document(policy_document)
        self.Policies.append(policy)


if __name__ == '__main__':
    t = Template()

    account_number = t.add_parameter(Parameter(
        "AccountNumber",
        Description="The name of the account number for the cross account Role",
        Type="String",
    ))

    iam_role = MyRole("CrossAccountS3Role")
    # Rack IAM is able to handle class like Troposphere functions such
    # as Ref() and Join()
    iam_role.add_account_assume_policy(
        Join(":", ["arn", "aws", "iam", "", Ref(account_number), "root"])
    )
    iam_role.add_policy(
        "CrossAccountS3Policy",
        "Allow",
        ["s3:*"]
    )
    cross_account_s3_role = t.add_resource(iam_role)
    t.add_output(Output(
        "RoleArn",
        Description="ARN of the role",
        Value=GetAtt(cross_account_s3_role, "Arn")))

    # Sample output is included in `iam_troposphere_integration.template`
    print(t.to_json())

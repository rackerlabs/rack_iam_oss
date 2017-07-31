from rack_iam import Role
from rack_iam import PolicyDocument, InlinePolicy
from rack_iam import Statement


# While objects should be created properly the first time,
# there may be instances such as user input data where that
# may not be possible. In such cases a few of the functional style
# parts of Python can be used to manipulate things:
myRole = Role('TestRole').set_assume_policy(
    PolicyDocument().add_statement(
        Statement('Allow', 'sts:AssumeRole').set_service_principal(
            ['lambda.amazonaws.com']
        )
    )
).add_policy(
    InlinePolicy('MyPolicy').set_policy_document(
        PolicyDocument().add_statements([
            Statement('Allow', 's3:*', '*'),
            Statement('Allow', 'es:*', '*'),
            Statement('Deny', 'ec2:*', '*', sid='DenyEc2')
        ])
    )
)

myRole.policies[0].policy_document.statements =\
    filter((lambda x: x.sid != 'DenyEc2'),
           myRole.policies[0].policy_document.statements)

print(len(myRole.policies[0].policy_document.statements))
print(myRole.policies[0].policy_document.statements[0].action)
print(myRole.policies[0].policy_document.statements[1].action)

# python mutation.py
# 2
# s3:*
# es:*

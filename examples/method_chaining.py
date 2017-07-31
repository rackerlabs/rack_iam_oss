from rack_iam import Role
from rack_iam import PolicyDocument, InlinePolicy
from rack_iam import Statement

# In some cases standard object construction can lead to a lot of temporary
# variables. For example:
myRole = Role('TestRole')

assumed_policy_doc = PolicyDocument()
lambda_assume = Statement('Allow', 'sts:AssumeRole')
lambda_assume.set_service_principal(['lambda.amazonaws.com'])
assumed_policy_doc.add_statement(lambda_assume)
myRole.set_assume_policy(assumed_policy_doc)

all_s3_policy = InlinePolicy('AllS3')
all_s3_doc = PolicyDocument()
all_s3_permissions = Statement('Allow', 's3:*', '*')
all_s3_doc.add_statement(all_s3_permissions)
all_s3_policy.set_policy_document(all_s3_doc)

myRole.add_policy(all_s3_policy)

# This can get pretty cumbersome and hard to read. To avoid the use of temporary
# variables for one time type assignment you can use method chaining like so:
myOtherRole = Role('TestRole').set_assume_policy(
    PolicyDocument().add_statement(
        Statement('Allow', 'sts:AssumeRole').set_service_principal(
            ['lambda.amazonaws.com']
        )
    )
).add_policy(
    InlinePolicy('AllS3').set_policy_document(
        PolicyDocument().add_statement(
            Statement('Allow', 's3:*', '*')
        )
    )
)

# This is a lot easier to work with, and more closely matches the structure
# of an IAM role. Of course these methods also work on various object attributes
# so modification after the fact is also possible
myOtherRole.policies[0].policy_document.statements.append(
    Statement('Allow', 'es:*', '*')
)

# With that in mind this will hopefully allow you to integrate the framework
# easily with other code. Note that method chaining is only supported on
# set/add type functions and will not work with get methods due to needing to
# return a specific type of data (string in most cases)

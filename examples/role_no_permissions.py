# This is a use case for blank policy roles, allowing the user to easily
# add permissions later (for example Redshift accessing an S3 bucket to
# import data).
from rack_iam import Role
from rack_iam import PolicyDocument
from rack_iam import Statement

redshift_role = Role("RedshiftRole")

asdoc = PolicyDocument()
astatement = Statement(
    "Allow", ["sts:AssumeRole"]
)
astatement.set_service_principal(
    ["redshift.amazonaws.com"]
)
asdoc.add_statement(astatement)
redshift_role.set_assume_policy(asdoc)

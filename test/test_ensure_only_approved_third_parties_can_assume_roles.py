import unittest

from cloudrail.knowledge.context.aws.account.account import Account
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.iam.policy import AssumeRolePolicy
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.iam.role import Role
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity

from src.ensure_only_approved_third_parties_can_assume_roles import EnsureOnlyAssumesThirdPartiesCanAssumeRoles

class TestEnsureOnlyAssumesThirdPartiesCanAssumeRoles(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureOnlyAssumesThirdPartiesCanAssumeRoles()

    def test_ensure_only_approved_third_parties_can_assume_roles_fail(self):
        # Arrange
        context = AwsEnvironmentContext()

        account = Account("a", "b", False)
        context.accounts.append(account)

        role = Role("a", "don't know", "not_approved_role", [], "not_approved_role", None, None)
        context.roles.append(role)

        principal = Principal(principal_type = PrincipalType.AWS, principal_values = ["arn:aws:iam::123456789012:root"])

        role_assume_policy = AssumeRolePolicy(account.account_name, role.role_name,
                 role.arn, [PolicyStatement(
                 StatementEffect.ALLOW,
                 ["assume role etc"],
                 ["*"],
                 principal,
                 'test123',)], "")
        role.assume_role_policy = role_assume_policy

        # Act
        result = self.rule.run(context, {})

        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_ensure_only_approved_third_parties_can_assume_roles_pass(self):
        # Arrange
        context = AwsEnvironmentContext()

        account = Account("a", "b", False)
        context.accounts.append(account)

        role = Role("a", "don't know", "not_approved_role", [], "not_approved_role", None, None)
        context.roles.append(role)

        principal = Principal(principal_type=PrincipalType.AWS, principal_values=["arn:aws:iam::645376637575:root"])

        role_assume_policy = AssumeRolePolicy(account.account_name, role.role_name,
                                              role.arn, [PolicyStatement(
                StatementEffect.ALLOW,
                ["assume role etc"],
                ["*"],
                principal,
                'test123', )], "")
        role.assume_role_policy = role_assume_policy

        # Act
        result = self.rule.run(context, {})

        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

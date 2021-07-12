import unittest

from cloudrail.knowledge.context.aws.account.account import Account
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.iam.policy import AssumeRolePolicy
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.iam.role import Role
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity

from src.ensure_only_approved_regions_are_used import EnsureOnlyApprovedRegionsAreUsed

class TestEnsureOnlyApprovedRegionsAreUsed(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureOnlyApprovedRegionsAreUsed()

    def test_bad_region(self):
        # Arrange
        context = AwsEnvironmentContext()

        ec2 = Ec2Instance("", "us-west-1", "", "", None, "", "", "", "", "", "", "", "", "", {})
        context.ec2s.append(ec2)

        # Act
        result = self.rule.run(context, {})

        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_good_region(self):
        # Arrange
        context = AwsEnvironmentContext()

        ec2 = Ec2Instance("", "us-east-1", "", "", None, "", "", "", "", "", "", "", "", "", {})
        context.ec2s.append(ec2)

        # Act
        result = self.rule.run(context, {})

        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

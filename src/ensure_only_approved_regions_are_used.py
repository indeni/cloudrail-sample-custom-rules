from typing import List, Dict
from cloudrail.knowledge.context.aws.account.account import Account
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils import arn_utils


class EnsureOnlyApprovedRegionsAreUsed(BaseRule):
    def __init__(self):
        self.approved_list_of_regions: List[str] = [
            "us-east-1",
            "eu-central-1",
            "GLOBAL_REGION" # For IAM
        ]

    def get_id(self) -> str:
        return 'ensure_only_approved_regions_are_used'

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def execute(self, env_context: BaseEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for resource in env_context.get_all_mergeable_resources():
            if isinstance(resource, AwsResource):
                if resource.region not in self.approved_list_of_regions:
                    issues.append(Issue(f'Resource is in region `{resource.region}` which is not approved for usage', resource, resource))
        return issues

    def should_run_rule(self, environment_context: BaseEnvironmentContext) -> bool:
        return True

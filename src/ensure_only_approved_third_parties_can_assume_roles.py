from typing import List, Dict
from cloudrail.knowledge.context.aws.account.account import Account
from cloudrail.knowledge.context.aws.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils import arn_utils


class EnsureOnlyAssumesThirdPartiesCanAssumeRoles(BaseRule):
    def __init__(self):
        self.approved_list_of_third_parties: List[str] = [
            "645376637575",  # Indeni Cloudrail
            "464622532012",  # DataDog
        ]

    def get_id(self) -> str:
        return 'ensure_only_approved_third_parties_can_assume_roles'

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for role in env_context.roles:
            for statement in role.assume_role_policy.statements:
                if statement.effect == StatementEffect.ALLOW:
                    for principal in statement.principal.principal_values:
                        if arn_utils.is_valid_arn(principal) and arn_utils.get_arn_account_id(principal) not in self.approved_list_of_third_parties:
                            issues.append(Issue(f'The IAM role `{role.get_friendly_name()}` has a trust policy that allows account `{ arn_utils.get_arn_account_id(principal)}` '
                                        f'to assume it but that is not in the list of pre-approved third-party accounts', role, role))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.roles)

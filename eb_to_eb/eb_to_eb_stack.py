from aws_cdk import (
    CfnOutput,
    Stack,
    aws_events_targets as events_target,
    aws_events as events,
    aws_logs as logs,
    aws_sqs as sqs,
)
from constructs import Construct


class EbToEbStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Add event buses
        events_bus_a = events.EventBus(self, "EventsBusA")
        events_bus_b = events.EventBus(self, "EventsBusB")

        # Dead Letter Queues
        dlq_a = sqs.Queue(self, "DLQForBusA")
        dlq_b = sqs.Queue(self, "DLQForBusB")

        # Add catch all log groups
        catch_all_log_group_a = logs.LogGroup(
            self, "CatchAllLogGroupA", retention=logs.RetentionDays.ONE_DAY
        )
        catch_all_log_group_b = logs.LogGroup(
            self, "CatchAllLogGroupB", retention=logs.RetentionDays.ONE_DAY
        )

        # Add event bus rule to match all the events
        event_bus_rule_a = events.Rule(
            self,
            "eventRuleForLogGroupA",
            event_bus=events_bus_a,
            event_pattern=events.EventPattern(version=["0"]),
        )

        # Add Cloudwatch as one target for the rule
        event_bus_rule_a.add_target(
            events_target.CloudWatchLogGroup(catch_all_log_group_a)
        )
        # Add the other event bus as another target for the rule
        event_bus_rule_a.add_target(
            events_target.EventBus(event_bus=events_bus_b, dead_letter_queue=dlq_a)
        )

        # Add event bus rule to match all the events
        event_bus_rule_b = events.Rule(
            self,
            "eventRuleForLogGroupB",
            event_bus=events_bus_b,
            event_pattern=events.EventPattern(version=["0"]),
        )

        # Add Cloudwatch as one target for the rule
        event_bus_rule_b.add_target(
            events_target.CloudWatchLogGroup(catch_all_log_group_b)
        )
        # Add the other event bus as another target for the rule
        event_bus_rule_b.add_target(
            events_target.EventBus(event_bus=events_bus_a, dead_letter_queue=dlq_b)
        )

        # Output
        CfnOutput(self, "EventBusA", value=events_bus_a.event_bus_arn)
        CfnOutput(self, "EventBusB", value=events_bus_b.event_bus_arn)
        CfnOutput(self, "SQS Queue A", value=dlq_a.queue_name)
        CfnOutput(self, "SQS Queue B", value=dlq_b.queue_name)
        CfnOutput(self, "Log Gruoup A", value=catch_all_log_group_a.log_group_name)
        CfnOutput(self, "Log Gruoup B", value=catch_all_log_group_b.log_group_name)

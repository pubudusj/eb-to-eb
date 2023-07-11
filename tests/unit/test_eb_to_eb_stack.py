import aws_cdk as core
import aws_cdk.assertions as assertions

from eb_to_eb.eb_to_eb_stack import EbToEbStack

# example tests. To run these tests, uncomment this file along with the example
# resource in eb_to_eb/eb_to_eb_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EbToEbStack(app, "eb-to-eb")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

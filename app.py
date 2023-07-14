#!/usr/bin/env python3
import os

import aws_cdk as cdk

from eb_to_eb.eb_to_eb_stack import EbToEbStack

app = cdk.App()
EbToEbStack(app, "EbToEbStack")

app.synth()

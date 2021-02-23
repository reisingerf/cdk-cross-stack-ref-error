#!/usr/bin/env python3
import os
import boto3
from aws_cdk import core
from stacks.slack import CodeBuildLambdaStack
from stacks.cicd import CICDStack

ssm_client = boto3.client('ssm')

account_id = os.environ.get('CDK_DEFAULT_ACCOUNT')
aws_region = os.environ.get('CDK_DEFAULT_REGION')
aws_env = {'account': account_id, 'region': aws_region}


cicd_dev_props = {
    'namespace': 'debug-cicd',
    'codebuild_project_name': 'debug_codebuild_project'
}

slack_dev_props = {
    'namespace': 'debug-codebuild-slack',
    'aws_account': aws_env['account']
}

app = core.App()

cicd = CICDStack(
    app,
    cicd_dev_props['namespace'],
    cicd_dev_props,
    env=aws_env
)
cb_project = cicd.cb_project
slack_dev_props['cb_project'] = cb_project
CodeBuildLambdaStack(
    app,
    slack_dev_props['namespace'],
    slack_dev_props,
    env=aws_env
)
app.synth()

from aws_cdk import (
    aws_codebuild as cb,
    aws_sns as sns,
    core
)


class CodeBuildLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ################################################################################
        # Create a reference to the UMCCRise CodeBuild project
        cb_project = cb.Project.from_project_name(	
            self,	
            id=props['codebuild_project_name'],	
            project_name=props['codebuild_project_name']	
        )	


        ################################################################################
        # Create an SNS topic to receive CodeBuild state change events
        topic_name = 'DebugCodeBuildSnsTopic'
        sns_topic = sns.Topic(
            self,
            id=topic_name,
            display_name=topic_name,
            topic_name=topic_name
        )
        sns_topic.grant_publish(cb_project)


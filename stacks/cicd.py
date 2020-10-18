from aws_cdk import (
    aws_codebuild as cb,
    aws_iam as iam,
    core
)

# As semver dictates: https://regex101.com/r/Ly7O1x/3/
semver_tag_regex = '(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'


class CICDStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        build_env = cb.BuildEnvironment(
            build_image=cb.LinuxBuildImage.from_docker_registry("docker:dind"),
            privileged=True,
            compute_type=cb.ComputeType.LARGE)

        cb_project = cb.Project(
            self,
            id="DebugCodeBuildProject",
            project_name=props['codebuild_project_name'],
            environment=build_env,
            timeout=core.Duration.hours(3),
            source=cb.Source.git_hub(
                identifier="umccrise",
                owner="umccr",
                repo="umccrise",
                clone_depth=1
            )
        )

        # Tackle IAM permissions
        # https://stackoverflow.com/questions/38587325/aws-ecr-getauthorizationtoken/54806087
        cb_project.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEC2ContainerRegistryPowerUser')
        )

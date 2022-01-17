# pylint: skip-file
name = "silex_blender"
version = "0.1.0"

authors = ["ArtFx TD gang"]

description = """
    Set of python module and blender config to integrate blender in the silex pipeline
    Part of the Silex ecosystem
    """

vcs = "git"


def commands():
    """
    Set the environment variables for silex_blender
    """
    env.SILEX_ACTION_CONFIG.prepend("{root}/addons/silex_blender/config")
    env.PYTHONPATH.append("{root}/addons")

    # Add the package to the scripts search path of Blender
    # Blender will look for startup and addons folders
    env.BLENDER_USER_SCRIPTS = "{root}"


@late()
def requires():
    silex_requirement = ["silex_client"]
    major = str(this.version.major)

    if major in ["dev", "beta", "prod"]:
        silex_requirement = [f"silex_client-{major}"]

    return ["blender", "python-3.9"] + silex_requirement

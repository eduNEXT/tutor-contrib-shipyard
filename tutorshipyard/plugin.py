from __future__ import annotations

import os
import os.path
from glob import glob

import click
import pkg_resources
from tutor import hooks

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

config = {
    # Add here your new settings
    "defaults": {
        "VERSION": __version__,
        "AUTO_TLS": True,
        # "CMS_LIMIT_CPU": 1,
        # "CMS_LIMIT_MEMORY": "2Gi",
        # "CMS_MAX_REPLICAS": 3,
        # "CMS_MIN_REPLICAS": 3,
        # "CMS_REQUEST_CPU": "600m",
        # "CMS_REQUEST_MEMORY": "1Gi",
        # "CMS_TARGET_CPU": 90,
        # "CMS_WORKERS_MAX_REPLICAS": 3,
        # "CMS_WORKERS_MIN_REPLICAS": 1,
        # "CMS_WORKERS_TARGET_CPU": 90,
        # "CMS_WORKER_LIMIT_CPU": 1,
        # "CMS_WORKER_LIMIT_MEMORY": "2Gi",
        # "CMS_WORKER_REQUEST_CPU": "600m",
        # "CMS_WORKER_REQUEST_MEMORY": "1Gi",
        # "ENABLE_OVERRIDES": False,
        # "FLOWER": False,
        # "ENABLE_RESOURCE_MANAGEMENT": False,
        "INGRESS": False,
        "INGRESS_EXTRA_HOSTS": [],
        # "LMS_LIMIT_CPU": 1,
        # "LMS_LIMIT_MEMORY": "2Gi",
        # "LMS_MAX_REPLICAS": 1,
        # "LMS_MIN_REPLICAS": 1,
        # "LMS_REQUEST_CPU": "600m",
        # "LMS_REQUEST_MEMORY": "1Gi",
        # "LMS_TARGET_CPU": 90,
        # "LMS_WORKERS_MAX_REPLICAS": 3,
        # "LMS_WORKERS_MIN_REPLICAS": 1,
        # "LMS_WORKERS_TARGET_CPU": 90,
        # "LMS_WORKER_LIMIT_CPU": 1,
        # "LMS_WORKER_LIMIT_MEMORY": "2Gi",
        # "LMS_WORKER_REQUEST_CPU": "600m",
        # "LMS_WORKER_REQUEST_MEMORY": "1Gi",
        # "NEWRELIC": False,
        # "NEWRELIC_CONFIG": "",
        "CUSTOM_CERTS": {},
        # "INIT_JOBS": False,
        # "FORUM_LIMIT_MEMORY": "1Gi",
        # "FORUM_LIMIT_CPU": 1,
        # "FORUM_REQUEST_MEMORY": "300Mi",
        # "FORUM_REQUEST_CPU": "200m",
        # "FORUM_MAX_REPLICAS": 1,
        # "FORUM_MIN_REPLICAS": 1,
        # "FORUM_TARGET_CPU": 90,
        # "DEBUG": False,
        # "OPENEDX_DEBUG_COOKIE": "ednx_enable_debug",
        # "CMS_SSO_USER": "cms"
    },
    # Add here settings that don't have a reasonable default for all users. For
    # instance: passwords, secret keys, etc.
    "unique": {
        # "SECRET_KEY": "\{\{ 24|random_string \}\}",
    },
    # Danger zone! Add here values to override settings from Tutor core or other plugins.
    "overrides": {
        "PLATFORM_NAME": "My platform as defined in plugin.py",
    },
}

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"SHIPYARD_{key}", value)
        for key, value in config["defaults"].items()
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'TUTOR_CONTRIB_SHIPYARD_'.
        # For example:
        ### ("TUTOR_CONTRIB_SHIPYARD_SECRET_KEY", "{{ 24|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair: (setting_name, new_value). For example:
        ### ("PLATFORM_NAME", "My platform"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################

# To add a custom initialization task, create a bash script template under:
# tutorshipyard/templates/tutor-contrib-shipyard/jobs/init/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    # For example, to add LMS initialization steps, you could add the script template at:
    # tutorshipyard/templates/tutor-contrib-shipyard/jobs/init/lms.sh
    # And then add the line:
    ### ("lms", ("tutor-contrib-shipyard", "jobs", "init", "lms.sh")),
]


# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path in MY_INIT_TASKS:
    full_path: str = pkg_resources.resource_filename(
        "tutorshipyard", os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


########################################
# DOCKER IMAGE MANAGEMENT
########################################


# Images to be built by `tutor images build`.
# Each item is a quadruple in the form:
#     ("<tutor_image_name>", ("path", "to", "build", "dir"), "<docker_image_tag>", "<build_args>")
hooks.Filters.IMAGES_BUILD.add_items(
    [
        # To build `myimage` with `tutor images build myimage`,
        # you would add a Dockerfile to templates/tutor-contrib-shipyard/build/myimage,
        # and then write:
        ### (
        ###     "myimage",
        ###     ("plugins", "tutor-contrib-shipyard", "build", "myimage"),
        ###     "docker.io/myimage:{{ TUTOR_CONTRIB_SHIPYARD_VERSION }}",
        ###     (),
        ### ),
    ]
)


# Images to be pulled as part of `tutor images pull`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PULL.add_items(
    [
        # To pull `myimage` with `tutor images pull myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ TUTOR_CONTRIB_SHIPYARD_VERSION }}",
        ### ),
    ]
)


# Images to be pushed as part of `tutor images push`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PUSH.add_items(
    [
        # To push `myimage` with `tutor images push myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ TUTOR_CONTRIB_SHIPYARD_VERSION }}",
        ### ),
    ]
)


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutorshipyard", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutorshipyard/templates/shipyard/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/shipyard/build``.
    [
        ("shipyard/build", "plugins"),
        ("shipyard/apps", "plugins"),
        ("shipyard/k8s", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorshipyard/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorshipyard", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################

# A job is a set of tasks, each of which run inside a certain container.
# Jobs are invoked using the `do` command, for example: `tutor local do importdemocourse`.
# A few jobs are built in to Tutor, such as `init` and `createuser`.
# You can also add your own custom jobs:

# To add a custom job, define a Click command that returns a list of tasks,
# where each task is a pair in the form ("<service>", "<shell_command>").
# For example:
### @click.command()
### @click.option("-n", "--name", default="plugin developer")
### def say_hi(name: str) -> list[tuple[str, str]]:
###     """
###     An example job that just prints 'hello' from within both LMS and CMS.
###     """
###     return [
###         ("lms", f"echo 'Hello from LMS, {name}!'"),
###         ("cms", f"echo 'Hello from CMS, {name}!'"),
###     ]


# Then, add the command function to CLI_DO_COMMANDS:
## hooks.Filters.CLI_DO_COMMANDS.add_item(say_hi)

# Now, you can run your job like this:
#   $ tutor local do say-hi --name="edunext"


#######################################
# CUSTOM CLI COMMANDS
#######################################

# Your plugin can also add custom commands directly to the Tutor CLI.
# These commands are run directly on the user's host computer
# (unlike jobs, which are run in containers).

# To define a command group for your plugin, you would define a Click
# group and then add it to CLI_COMMANDS:


### @click.group()
### def tutor-contrib-shipyard() -> None:
###     pass


### hooks.Filters.CLI_COMMANDS.add_item(tutor-contrib-shipyard)


# Then, you would add subcommands directly to the Click group, for example:


### @tutor-contrib-shipyard.command()
### def example_command() -> None:
###     """
###     This is helptext for an example command.
###     """
###     print("You've run an example command.")


# This would allow you to run:
#   $ tutor tutor-contrib-shipyard example-command

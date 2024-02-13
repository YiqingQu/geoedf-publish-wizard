"""
JupyterHub config file enabling gist-access via environment variables

1. enable persisted auth_state
2. pass select auth_state to Spawner via environment variables
3. enable auth_state via `JUPYTERHUB_CRYPT_KEY` and `enable_auth_state = True`
"""

import os
import pprint
import warnings

from jupyterhub.auth import DummyAuthenticator
from nb.log import log, log_handler


# define our OAuthenticator with `.pre_spawn_start`
# for passing auth_state into the user environment


class CILogonEnvAuthenticator(DummyAuthenticator):
    async def pre_spawn_start(self, user, spawner):
        auth_state = await user.get_auth_state()
        # pprint.pprint(auth_state)
        log.info(f"auth_state = {auth_state}")

        if not auth_state:
            # user has no auth state
            return

        # define some environment variables from auth_state
        spawner.environment['CILOGON_TOKEN'] = auth_state['access_token']
        spawner.environment['CILOGON_USER'] = auth_state['cilogon_user']['login']
        spawner.environment['CILOGON_EMAIL'] = auth_state['cilogon_user']['email']
#
# class GitHubEnvAuthenticator(GitHubOAuthenticator):
#     async def pre_spawn_start(self, user, spawner):
#         auth_state = await user.get_auth_state()
#         pprint.pprint(auth_state)
#
#         if not auth_state:
#             # user has no auth state
#             return
#
#         # define some environment variables from auth_state
#         spawner.environment['GITHUB_TOKEN'] = auth_state['access_token']
#         spawner.environment['GITHUB_USER'] = auth_state['github_user']['login']
#         spawner.environment['GITHUB_EMAIL'] = auth_state['github_user']['email']


c.DummyAuthenticator.scope = ['gist', 'user:email']
c.JupyterHub.authenticator_class = CILogonEnvAuthenticator

# enable authentication state
c.DummyAuthenticator.enable_auth_state = True

if 'JUPYTERHUB_CRYPT_KEY' not in os.environ:
    warnings.warn(
        "Need JUPYTERHUB_CRYPT_KEY env for persistent auth_state.\n"
        "    export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)"
    )
    c.CryptKeeper.keys = [os.urandom(32)]

# launch with Docker
c.JupyterHub.spawner_class = 'simplespawner.DockerSpawner'
c.JupyterHub.hub_ip = '0.0.0.0'
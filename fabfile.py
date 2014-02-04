# This is version 0.0.1 of the fabfile

import os
from __future__ import with_statement

from fabric.api import abort, cd, env, run
from fabric.contrib.console import confirm
from fabric.contrib.files import exists

CONFIG = {}

# Configure your deployment targets here

#CONFIG['staging'] = {
    #'ssh_user':           'static',
    #'domain':             'supertesthost.com',
    #'deploy_to':          '/home/example/staging.example.com',
    #'repository':         'git@supersourcecontrolteamgo.com:example.git',
    #'branch':             'staging',
    #'post_deploy_script': 'script/build',
    #'post_setup_script':  'script/build'
    #}

#CONFIG['production'] = {
    #'ssh_user':           'static',
    #'domain':             'supertesthost.com',
    #'deploy_to':          '/home/static/example.com',
    #'repository':         'git@supersourcecontrolteamgo.com:example.git',
    #'branch':             'master',
    #'post_deploy_script': 'script/build',
    #'post_setup_script':  'script/build'
    #}

# And don't touch anything below here

DEPLOY_TARGET=""

def _check_config():
    if len(CONFIG.keys()) == 0:
      abort("There are no deployment targets configured\nPlease consult the fabfile and add some targets")

def _ensure_config(target):
    if not target in CONFIG.keys():
      abort("There is no deployment target named '%s'" % target)

def target(target):
    _check_config()
    global DEPLOY_TARGET
    if not target:
        abort("You must tell me which deployment target to use")
    _ensure_config(target)
    DEPLOY_TARGET=target
    env.hosts.append(CONFIG[DEPLOY_TARGET]['domain'])
    env.user = CONFIG[DEPLOY_TARGET]['ssh_user']

def _check_deploy_target():
    if not DEPLOY_TARGET:
      abort("Specify a deployment target with the target task")

def setup():
    _check_config()
    _check_deploy_target()
    deploy_to = CONFIG[DEPLOY_TARGET]['deploy_to']
    base_dir, code_dir = os.path.split(deploy_to)
    if exists(deploy_to):
        abort("Path '%s' already exists.\nUse the deploy task instead" % deploy_to)
    else:
        with cd(base_dir):
            run("git clone %s %s" % (CONFIG[DEPLOY_TARGET]['repository'], code_dir))
        with cd(deploy_to):
            run("git fetch origin")
            run("git checkout %s" % CONFIG[DEPLOY_TARGET]['branch'])
            run("%s" % CONFIG[DEPLOY_TARGET]['post_setup_script'])

def deploy():
    _check_config()
    _check_deploy_target()
    deploy_to = CONFIG[DEPLOY_TARGET]['deploy_to']

    if not exists(deploy_to):
        abort("Path '%s' doesn't exist.\nYou need to run the setup task first" % deploy_to)

    with cd(deploy_to):
        run("git stash")
        run("git fetch origin")
        run("git pull origin %s" % CONFIG[DEPLOY_TARGET]['branch'])
        run("%s" % CONFIG[DEPLOY_TARGET]['post_deploy_script'])

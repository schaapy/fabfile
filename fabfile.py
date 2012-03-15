from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists

CONFIG = {}

# Configure your deployment targets here

CONFIG['staging'] = {
    'ssh_user':           'canvas',
    'domain':             'supertesthost.com',
    'deploy_to':          '/home/canvas/staging.fabtest.com',
    'repository':         'git://github.com/ess/fabtest.git',
    'branch':             'develop',
    'post_deploy_script': 'script/build',
    'post_setup_script':  'script/build'
    }

#CONFIG['production'] = {
    #'ssh_user':           'canvas',
    #'domain':             'supertesthost.com',
    #'deploy_to':          '/home/canvas/fabtest.com',
    #'repository':         'git://github.com/ess/fabtest.git',
    #'branch':             'master',
    #'post_deploy_script': 'script/build',
    #'post_setup_script':  'script/build'
    #}

# And don't touch anything below here

DEPLOY_TARGET=None

def _check_config():
  if len(CONFIG.keys()) == 0:
    abort("There are no deployment targets configured\nPlease consult the fabfile and add some targets")

def _ensure_config(target):
  if not target in CONFIG.keys():
    abort("There is no deployment target named '%s'" % target)

def target(target=None):
  _check_config()
  global DEPLOY_TARGET
  if target == None:
    abort("You must tell me which deployment target to use")
  _ensure_config(target)
  DEPLOY_TARGET=target
  env.hosts.append(CONFIG[DEPLOY_TARGET]['domain'])
  env.user = CONFIG[DEPLOY_TARGET]['ssh_user']

def _check_deploy_target():
  if DEPLOY_TARGET == None:
    abort("Specify a deployment target with the target task")

def setup():
  _check_config()
  _check_deploy_target()
  deploy_to = CONFIG[DEPLOY_TARGET]['deploy_to']
  base_dir = deploy_to.rpartition('/')[0]
  code_dir = deploy_to.rpartition('/')[2]
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

  with settings(warn_only = True):
    if run("test -d %s" % deploy_to).failed:
      abort("Path '%s' doesn't exist.\nYou need to run the setup task first", deploy_to)
  with cd(deploy_to):
    run("git stash")
    run("git fetch origin")
    run("git pull origin %s" % CONFIG[DEPLOY_TARGET]['branch'])
    run("%s" % CONFIG[DEPLOY_TARGET]['post_deploy_script'])

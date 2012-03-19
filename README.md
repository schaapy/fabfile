# Canvas Fabfile #

This is a fabfile that can be used for site/application deployment. It roughly
models the same process as
[whiskey_disk](https://github.com/flogic/whiskey_disk), but is not exactly a
drop-in replacement (probably uses more than 1 SSH connection, does not support
config repos).

## Contact Us ##

Having a problem with this fabfile? Feel free to drop us a line:

* Github Issues Page - https://github.com/canvas/fabfile/issues

# Configuration #

In order to use this fabfile, you will need to edit it a bit. If you look in
the source, you will see two CONFIG blocks that are commented out. These are
two separate deployment targets ("staging" and "production"). A deployment
target, generally, is defined as a dictionary:

<pre>CONFIG['target name'] = {
  'ssh_user': 'remote_user_name',
  'domain':   'remote_host_name',
  'deploy_to': '/path/to/which/you/want/to/deploy',
  'repository': 'the git repository from which to deploy',
  'branch': 'the branch from which to deploy',
  'post_deploy_script': 'a script relative to deploy_to to run after deploy',
  'post_setup_script': 'a script relative to deploy_to to run after setup'
}</pre>

At current, all of the configuration flags are required. For the case of the
post scripts, set them to empty strings ('') if you do not wish to run a script.

# Usage #

Now that you have your targets set up, you can start using the fabfile. So as
to conform to the whiskey disk user interface, the first thing that you'll need
to do is to set up your target. For example, if you have a "STAGING" target,
the setup looks like this (run from the directoy that contains your fabfile):

    fab target:STAGING setup

This command does an initial clone of the repo into the "deploy to" path on the
remote server, then it runs the post setup script. Technically, your app or site
is now deployed, depending on your definition of deployedness (which is now a
word). To really deploy (that is, update from the git repo and run the post
deploy script), deploy the target like so:

    fab target:STAGING deploy

# Release History #

* 0.0.1 - Cleaned up example targets, cleaned up some code, added README
* 0.0.0 - Initial release

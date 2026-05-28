Deploying a COAR 2 Masto service
================================

Configuring Mastodon API accesses
---------------------------------

COAR 2 Masto needs access to one or many Masotodon account(s)
in order to relay COAR notifications as posts.
Mastodon allows to specify "applications", which provide API access tokens,
usable by clients to post on behalf of the account.

To create a Mastodon API access token for COAR 2 Masto to use,
login  to the Mastodon account and browse to <masto_instance>/settings/applications

Click "New application", provide a name, and specify `write:statuses`
and `write:media` as allowed scopes.

Create a section for this Mastodon account in file `config.ini`
and copy the generated access token there (see `config.ini.sample`)


Running the service
-------------------

Once configured, the service can be run with the `./run` helper script.
The script expects to find a working Python virtual environment
in `$HOME/.virtualenvs/c2m` and then runs the service as a daemon,
storing the PID in file `run.pid`

Create a Python virtual environment for COAR 2 Masto e.g. with `mkvirtualenv`,
edit the script `./run` as needed to match the correct path - or make sure
you create the virtual environment there, or symlink.

Install Python requirements into the virtual env
with `pip install -r requirements.txt`

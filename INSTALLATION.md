# INSTALLATION
group_migrator requires a working python installation. The instructions below will work on Mac and Linux boxes. Windows users are on their own.

## System-wide installation
1. ``git pull https://github.com/burningmantech/mailman_group_migrator``
1. ``cd mailman_group_migrator``
2. ``sudo pip install -r requirements.txt``


## Using Virtualenv
1. ``wget https://github.com/burningmantech/mailman_group_migrator/archive/master.zip`` (or clone as in step 1 above)
2. ``unzip master.zip``
3. ``cd mailman_group_migrator``
4. ``virtualenv env``
5. ``source env/bin/activate``
6. ``pip install -r requirements.txt``

For this installation method, please note the following:

1.  You will have to enter this directory and type:

        $ source env/bin/activate (if you are using bash)
each time you start a new shell session.
2. The script must be exectuted via:

        $ python group_migrator.py
to avoid using the system python.



## Configuration

From there you can cd into the galias directory.

The Google OAuth2 APIs require a client_secrets.json file for storing various OAuth2 keys. If you are part of the burningman.org organization, contact one of the administrators for a link to the key.

Otherwise, follow the procedure at https://developers.google.com/api-client-library/python/auth/api-keys to generate the client keys and client_secrets.json file.

In order to save typing there is an config file you can store your
domain in. This can be passed on the command line or
prompted for if you don't provide it.

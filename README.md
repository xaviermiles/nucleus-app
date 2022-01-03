# home-server
Learning how to use flask to make a web app

The [run](#run.sh) bash script will start the app on local host - uncomment line 3 if running for the first time. Need a "./config.yaml" file with:
```
primary_user:
  username: <something>
  password: <something>
```
This primary/super user will be registered as a user when the sqlite database is initialised.

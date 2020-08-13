# Tweakly (branch: fast-deploy)
> Python 3.6+ | Fast, Simple & Secure API | powered by Flask and MongoDB

## Reintroduction
This is essentially Tweakly but stripped down and more agile.

It removes the heavy lifting of getting + parsing the Packages files from each repo and delegates this task to a cronjob instead!

#### Reasoning:
Primarily because this boosts the app's speed and footprint by basically making it a fancy and pure db lookup API

## Changes (fast-deploy <> master)
- Outsource repo updating task to `cronjob`
- smaller footprint
- pre-setup to use the "api" subdomain *(e.g. api.your.domain/v1/tweakly/)*
- uses Flask-Limiter to enforce API access restrictions

## Setup Infos
You can follow the regular Tweakly (branch: master) guide, however this is different:
- Granted you followed the original tutorial, you will have uwsgi installed. Else make sure you have uwsgi because this branch uses uwsgi. You can of course use whatever you want and adapt!
- You will also need to install `Flask-Limiter`
- Everything found in the *cronjob* folder can be put anywhere in your home dir and does not belong with the Flask-App/ the web dir
  - You will need to setup a proper cronjob!
    - This will help you: [cronjob guru](https://crontab.guru)
- A uwsgi compliant `.ini`  file will be included, however you will need to setup a systemd unit yourself
  - I recommend this tutorial by [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04)
  - You can of course change the included `.ini` to your liking

## why?
Because the flask-app shouldn't need todo something which a regular cronjob can do.

## Disclaimer
This branch is considered experimental due to its difference in comparison to the master, but I am running this exact setup myself and it's solid.

Your mileage may vary, in case of questions I am available on [Twitter](https://twitter.com/saadat603) or under saadatdev (at) gmail (dot) com
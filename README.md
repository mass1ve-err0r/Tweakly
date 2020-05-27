# Tweakly
> Python 3.6+ | Fast, Simple & Secure API | powered by Flask and MongoDB

## Introduction
Tweakly is a Flask-based app you can deploy to provide an endpoint to search tweaks and return them in a tidy JSON.

Tweakly is very barebone so there is no magic happening in regards to the cached tweaks: You have to ask Tweakly to update it's database so it updates them.

Currently the following repositories are scanned & indexed by default:
- Chariz
- Dynastic
- Packix
- Twickd

Tweak information are saved to a MongoDB Instance.
## Features
- Automatically parse entire repository
- Efficient & logic lookup (used regex: `^<TweakName>`)
- Expendable
	- Just add another `PackageManager` object inside the `LookupAPI.py` and the corresponding JSON fields to the functions, tada!
- Small footprint

## Prerequisites & Installation
### Prerequisites:
- Python 3.6+
- From PIP:
	- Flask
	- Flask-JWT-Extended
	- python-dotenv
	- PyMongo
- MongoDB
- A Flask -friendly WSGI
	- Look [HERE](https://flask.palletsprojects.com/en/1.1.x/deploying/) for examples and deployment guidance.

If you got everything, make sure a simple Flask "Hello World" runs and then proceed.
### Installation:
1. Deploy Flask to any WSGI of choice. The prerequisite should have this already covered, so Flask itself is already able to run.

2. Upload Tweakly to your server, configure to your liking and **before** launching, add back the function to obtain a token (in `LookupAPI.py`).

3. Launch for the Tweakly first time and get a token. Once you got the token, terminate Tweakly.

4. Since you have the token now, remove the function and then restart Tweakly.

Now you have a token for Tweakly and there's no way to recreate another token unless the Tweakly is terminated again and the procedure above is repeated.

This is solely done to avoid any further maintenance problems/ issues with Tweakly. Access is only granted to those who have a token.

## F.A.Q
- **_I need another token but Tweakly is already running !_**
	- Since the Tweaks are stored independently from Tweakly/ Flask, you can savely terminate Tweakly, go through the procedure found in installation and restart Tweakly.
- **_Someone has unauthorized access !_**
	- terminate Tweakly immediately and change your JWT Secret!
	
  This will ensure that each token will automatically be revoked. You will have to issue new tokens for each of your users.
- **_I want to include XY repository for my variant of Tweakly !_**
	- Easy, just add another `PackageManager`-object and add the according fields to the return JSON.
- **_Y no app-factory pattern ???_**
	- because this just isn't that big of a Flask-app lmao. Circular imports are dodged by importing in order.

## Return JSON Format
Example JSON for Gesto:
```json
{
	"dynastic": 
	[
			{
			"Author": "Alessandro Chiarlitti and Gabriele Filipponi",
			"Depiction": "https://repo.dynastic.co/depiction/260789741820051456/",
			"Description": "True Multitasking — See Gesto (cydia://package/com.blackhole.Gesto) for iOS 11/12 compatibility",
			"IconURL": "https://repo.dynastic.co/data/static/version/317726058596007936/317726058868637696?size=180",
			"Name": "Gesto for iOS 13",
			"Paid": true,
			"SileoURL": "sileo://package/com.blackhole.Gesto13",
			"Size": "792828",
			"Version": "1.1.1",
			"ZebraURL": "zbra://packages/com.blackhole.Gesto13"
			},
			{
			"Author": "Alessandro Chiarlitti and Gabriele Filipponi",
			"Depiction": "https://repo.dynastic.co/depiction/176619415092068352/",
			"Description": "True Multitasking — See Gesto for iOS 13 (cydia://package/com.blackhole.Gesto13) for iOS 13 compatibility.",
			"IconURL": "https://repo.dynastic.co/data/static/version/201365877868724224/201365878086828032?size=180",
			"Name": "Gesto for iOS 11/12",
			"Paid": true,
			"SileoURL": "sileo://package/com.blackhole.Gesto",
			"Size": "1158208",
			"Version": "1.3.2",
			"ZebraURL": "zbra://packages/com.blackhole.Gesto"
			}
	]
}
```
You basically get a JSON Object containing 4 potential lists with dictionaries inside representing Packages.

## Credits
- My swedish pigeon gang - y'all rock lmao
- My friends and family

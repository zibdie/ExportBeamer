# ExportBeamer

## Export your posts easily from Beamer (getbeamer.com)

Beamer makes it incredibly difficult to export your announcements in a neat and clean matter, this script should make the process simple and easy.

You will need:

- API Key of your Beamer account [can be found at https://app.getbeamer.com/settings#api ]
- Python 3.9+ [most likely will work on lower versions but not tested]

*If you have [Docker](https://www.docker.com/get-started/), you can use the prepared Dockerfile that comes with this repository*

The script prepares a simple HTML file with:
* Text Content	
* Raw HTML Content	
* Parsed HTML	
* Metadata

Metadata includes:
* Title
* Post URL	
* Date
* Negative Reactions	
* Neutral Reactions	
* Positive Reactions	
* Published
* Category
* Clicks
* Views
* Uniqueviews

All pictures are saved locally in case Beamer deletes them from their server.

## Using the Script Locally
Assuming you have Python 3.9 and above, its best you create a virtual environment and use that. See: https://docs.python.org/3/library/venv.html

Next, install the required libraries:
```
(venv) myuser> pip install --no-cache-dir -r requirements.txt
```

Then, rename the `.env.sample` to `.env` and add your [Beamer API key](https://app.getbeamer.com/settings#api)
```
(venv) myuser> mv .env.sample .env
(venv) myuser> cat .env
BEAMER_API_KEY=YOUR_KEY_HERE
```

Finally, run the script:
```
(venv) myuser> python beamer_export.py
```

The script does allow a export location to be specified:
```
(venv) myuser> python beamer_export.py --output-dir "C:\Users\myuser\myproject"
```

 
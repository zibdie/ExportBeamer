# ExportBeamer

[https://github.com/zibdie/ExportBeamer](https://github.com/zibdie/ExportBeamer)

## Export your posts easily from Beamer (getbeamer.com)

Beamer [https://www.getbeamer.com/] makes it incredibly difficult to export your announcements in a neat and clean matter. In fact, according to their support, you can only do that via their API which makes the barrier much higher for those who are not used to scraping. This script should make the process simple and easy.

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

When the script runs, it will prepare everything in an HTML file and all pictures are saved locally in case Beamer deletes them from their server. Therefore, you can technically view your announcements offline as, once exported, your announcements are independant from Beamer.

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
(venv) myuser> python export_beamer.py
```

The script does allow a export location to be specified:
```
(venv) myuser> python export_beamer.py --output-dir "C:\Users\myuser\myproject"
```

## Running through Docker

The latest image is available through DockerHub. You can get started instantly by running:
```
docker run -e BEAMER_API_KEY=<YOUR BEAMER KEY HERE> -v ./output:/app/output zibdie/exportbeamer:latest
```

You can run it locally by running this one command in this project's directory after you have cloned it to your machine:
```
docker build -t export_beamer . && docker run -e BEAMER_API_KEY=<YOUR BEAMER KEY HERE> -v /path/to/local/output:/app/output export_beamer
```
*You can ommit the `-e` in the command and put your key in the .env file*

import requests, os, datetime
from bs4 import BeautifulSoup

BEAMER_API_KEY = os.environ.get("BEAMER_API_KEY") or None


def savePosts():
    if not BEAMER_API_KEY or BEAMER_API_KEY == "":
        raise Exception("BEAMER_API_KEY is not set. Check your environment variables.")
    r = requests.get(
        "https://api.getbeamer.com/v0/posts?maxResults=500",
        headers={
            "Beamer-Api-Key": BEAMER_API_KEY,
        },
    )

    if r.status_code != 200:
        raise Exception("Error fetching posts from Beamer API")
    r = r.json()
    html = BeautifulSoup(
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div id="content"></div>
</body>
</html>""",
        "html.parser",
    )
    html.find(
        "title"
    ).string = (
        f"Beamer Export Announcements - {datetime.datetime.now().strftime('%Y-%m-%d')}"
    )
    for post in r:
        return

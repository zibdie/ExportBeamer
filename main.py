import requests, os, datetime, shutil, html
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
BEAMER_API_KEY = os.getenv("BEAMER_API_KEY") or None


def savePosts():
    def create_metadata_row(label, value):
        row = BeautifulSoup("", "html.parser").new_tag("tr")
        label_td = BeautifulSoup("", "html.parser").new_tag("td")
        value_td = BeautifulSoup("", "html.parser").new_tag("td")
        label_td.string = label
        value_td.string = str(value)
        row.append(label_td)
        row.append(value_td)
        return row

    if not BEAMER_API_KEY:
        raise Exception("BEAMER_API_KEY is not set. Check your environment variables.")

    response = requests.get(
        "https://api.getbeamer.com/v0/posts?maxResults=500",
        headers={"Beamer-Api-Key": BEAMER_API_KEY},
    )

    if response.status_code != 200:
        raise Exception("Error fetching posts from Beamer API")

    posts = response.json()

    # Create output and imgs directories
    output_dir = "output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=False, onerror=None)
    imgs_dir = os.path.join(output_dir, "imgs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(imgs_dir):
        os.makedirs(imgs_dir)

    # Clear the output directory
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    soup = BeautifulSoup(
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                td, th {{
                    border: 1px solid black;
                    padding: 8px;
                }}
                textarea {{
                    width: 100%;
                    height: 100px;
                }}
                .post-div {{
                    margin-top: 20px;
                    margin-bottom: 20px;
                }}
            </style>
            <title>Beamer Export Announcements - {datetime.datetime.now().strftime('%Y-%m-%d')}</title>
        </head>
        <body>
            <div id="content"></div>
        </body>
        </html>""",
        "lxml",
    )

    content_div = soup.find("div", {"id": "content"})

    for post in posts:
        post_div = soup.new_tag(
            "div", attrs={"id": str(post["id"]), "class": "post-div"}
        )
        table = soup.new_tag("table")
        post_div.append(table)

        # Parse the raw HTML content
        parsed_html = BeautifulSoup(
            post["translations"][0]["contentHtml"], "html.parser"
        )

        # Process each image in the parsed HTML
        for img_count, img_tag in enumerate(parsed_html.find_all("img"), start=1):
            img_url = img_tag["src"]
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                img_filename = f"{post['id']}-{img_count}.png"
                img_path = os.path.join(imgs_dir, img_filename)
                with open(img_path, "wb") as img_file:
                    img_file.write(img_response.content)
                img_tag["src"] = os.path.join("imgs", img_filename)

        post["translations"][0]["contentHtml"] = str(parsed_html)

        text_row = soup.new_tag("tr")
        text_title = soup.new_tag("td")
        text_title.string = "Text Content"
        text_content = soup.new_tag("td")
        text_area = soup.new_tag("textarea")
        text_area.string = post["translations"][0]["content"]
        text_content.append(text_area)
        text_row.append(text_title)
        text_row.append(text_content)
        table.append(text_row)

        html_row = soup.new_tag("tr")
        html_title = soup.new_tag("td")
        html_title.string = "Raw HTML Content"
        html_content = soup.new_tag("td")
        html_area = soup.new_tag("textarea")
        html_area.string = post["translations"][0]["contentHtml"]
        html_content.append(html_area)
        html_row.append(html_title)
        html_row.append(html_content)
        table.append(html_row)

        parsed_html_row = soup.new_tag("tr")
        parsed_html_title = soup.new_tag("td")
        parsed_html_title.string = "Parsed HTML"
        parsed_html_content = soup.new_tag("td")
        parsed_html = BeautifulSoup(
            post["translations"][0]["contentHtml"], "html.parser"
        )
        parsed_html_content.append(parsed_html)
        parsed_html_row.append(parsed_html_title)
        parsed_html_row.append(parsed_html_content)
        table.append(parsed_html_row)

        metadata_row = soup.new_tag("tr")
        metadata_title = soup.new_tag("td")
        metadata_title.string = "Metadata"
        metadata_content_td = soup.new_tag("td")
        metadata_table = soup.new_tag("table")

        metadata_fields = [
            "date",
            "negativeReactions",
            "neutralReactions",
            "positiveReactions",
            "published",
            "category",
            "clicks",
            "views",
            "uniqueViews",
        ]

        metadata_table.append(
            create_metadata_row("Title", post["translations"][0]["title"])
        )
        metadata_table.append(
            create_metadata_row("Post URL", post["translations"][0]["postUrl"])
        )

        for field in metadata_fields:
            metadata_table.append(
                create_metadata_row(
                    field.replace("Reactions", " Reactions").title(), post[field]
                )
            )

        metadata_content_td.append(metadata_table)
        metadata_row.append(metadata_title)
        metadata_row.append(metadata_content_td)
        table.append(metadata_row)
        content_div.append(post_div)

    soup.prettify()
    with open(
        os.path.join(
            "output",
            f"beamer_export_{datetime.datetime.now().strftime('%Y-%m-%d')}.html",
        ),
        "w",
        encoding="utf-8",
    ) as file:
        file.write(str(soup))


savePosts()

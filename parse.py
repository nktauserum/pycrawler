import trafilatura
import json

class Data:
    def __init__(self, title, sitename, text):
        self.title = title
        self.sitename = sitename
        self.text = text

    def json(self):
        return {
            "title":    self.title
        }

def _extract_from_url(url):
    downloaded = trafilatura.fetch_url(url)
    result = trafilatura.extract(downloaded, include_formatting=False, include_links=False, include_images=False, include_tables=False, only_with_metadata=True, output_format='json')
    if result:
        result_dict = json.loads(result)
        return Data(result_dict["title"], result_dict["source-hostname"], result_dict["raw_text"])
    return None

def extract(url):
    if not url.startswith("https://web.archive.org"):
        result = _extract_from_url(url)
        if result:
            return result
        else:
            print(f"empty result for {url}")
            new_url = "https://web.archive.org/web/20/" + url
            return _extract_from_url(new_url)
    return None
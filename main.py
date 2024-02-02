import os
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

pattern = r'\[(\w+-\d+)\]'
baseSearchLink = "https://www.subtitlecat.com/index.php?search="
baseLink = "https://www.subtitlecat.com/"
basePath = "<basePath to folder with videos>"


def listDisk(path: str) -> list:
    files = os.listdir(path)
    for file in files:
        print(file)
    return files


def main():
    files = listDisk(basePath)
    codes = []

    for file in files:
        match = re.search(pattern, file)
        if match:
            print(f"Found: {match.group(1)} in {file}")
            codes.append({
                "code": match.group(1),
                "file": file
                })

    for fileDict in tqdm(codes):
        code = fileDict["code"]
        filename = fileDict["file"].rsplit(".", 1)[0]
        print(f"processing code: {code}...")
        url = baseSearchLink + code
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.find_all('a', href=True)
        for link in links:
            if code in link.get('href'):
                subURL = baseLink + link.get('href')
                print("\t" + subURL)
                r = requests.get(subURL)
                subSoup = BeautifulSoup(r.text, "html.parser")
                downloadLinks = subSoup.find_all('a', id='download_en')
                for downloadLink in downloadLinks:
                    print("\t\t" + baseLink + downloadLink.get('href'))
                    response = requests.get(baseLink + downloadLink.get('href'))
                    if response.status_code == 200:
                        with open(basePath + filename+".srt", 'wb') as file:
                            file.write(response.content)
                        print(f"Downloaded {filename}")
                    else:
                        print(f"Error: {response.status_code}")


if __name__ == '__main__':
    main()

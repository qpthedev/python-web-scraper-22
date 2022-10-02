from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

browser = webdriver.Chrome(options=options)

browser.get("https://www.indeed.com/jobs?q=python")

results = []
soup = BeautifulSoup(browser.page_source, "html.parser")
job_list = soup.find("ul", class_="jobsearch-ResultsList")
jobs = job_list.find_all("li", recursive=False)
for job in jobs:
    zone = job.find("div", class_="mosaic-zone")
    if zone == None:
        anchor = job.select_one("h2 a")
        title = anchor.find("span")["title"]
        link = anchor["href"]
        company = job.find("span", class_="companyName")
        location = job.find("div", class_="companyLocation")

        job_data = {
            "link": f"https://www.indeed.com{link}",
            "company": company.string,
            "location": location.string,
            "position": title,
        }

        results.append(job_data)

for result in results:
    print(result, "///////////\n")

from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

browser = webdriver.Chrome(options=options)

browser.get("https://www.indeed.com/jobs?q=python")

soup = BeautifulSoup(browser.page_source, "html.parser")
job_list = soup.find("ul", class_="jobsearch-ResultsList")
jobs = job_list.find_all("li", recursive=False)
for job in jobs:
    print(job)
    print("///////////////////////")

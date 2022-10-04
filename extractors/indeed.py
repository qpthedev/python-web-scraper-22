from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_page_count(keyword):
    base_url = "https://www.indeed.com/jobs"

    options = webdriver.ChromeOptions()
    # added options to reduce log clutter
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(options=options)
    browser.get(f"{base_url}?q={keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", attrs={"aria-label": "pagination"})

    # return 1 if there is only one page
    if pagination == None:
        return 1

    pages = pagination.select("div a")
    count = len(pages)

    if count > 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    base_url = "https://www.indeed.com/jobs"
    pages = get_page_count(keyword)
    results = []
    for page in range(pages):
        final_url = f"{base_url}?q={keyword}&start={page*10}"
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        browser = webdriver.Chrome(options=options)
        browser.get(final_url)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor.find("span")["title"]
                link = anchor["href"]
                company = job.find("span", class_="companyName").string
                location = job.find("div", class_="companyLocation").string

                job_data = {
                    "link": f"https://www.indeed.com{link}",
                    "company": company,
                    "location": location,
                    "position": title,
                }
                # for cases where some entries of the job posting is left blank
                for entry in job_data:
                    if job_data[entry] != None:
                        job_data[entry].replace(",", " ")

                results.append(job_data)
    return results

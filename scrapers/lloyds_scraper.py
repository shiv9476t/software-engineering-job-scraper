import requests
import time
from scrapers.base_scraper import BaseScraper
from job import Job
import json

class LloydsScraper(BaseScraper):

    def __init__(self):
        super().__init__(
            company_name = "Lloyds",
            base_url = "https://www.lloydsbankinggroup.com/careers/job-search/jcr:content/par/c_106_grid_layout/col_1/par/c_119_fragment_resul.results.json"
        )

    def scrape_jobs(self, search_term="software engineering"):
        jobs_list = []
        page = 0
        
        while True:
            params = {
                "t": search_term,
                "f": f"SearchTerm:{search_term}!allLocation:!jobCategory:!workerType:!postedDate:",
                "p": page
            }

            response = requests.get(self.base_url, params=params)
            if response.status_code != 200:
                break

            data = response.json()
            jobs = data.get("fragments", [])

            if not jobs:
                break

            for job_data in jobs:
                job = self.parse_job(job_data)
                if job:
                    jobs_list.append(job)

            page += 1
            time.sleep(1)

        return jobs_list

    def parse_job(self, job_data):
        title = job_data["fields"][10]["value"]
        location = job_data["fields"][3]["value"]
        salary = job_data["fields"][4]["value"]
        reference = job_data["fields"][5]["value"]
        url = f"https://www.lloydsbankinggroup.com/careers/job-search/job-details.html?reference={reference}"

        if not title or not url:
            return None
        
        job_object = Job(self.company_name, title, location, salary, url)
        
        return job_object


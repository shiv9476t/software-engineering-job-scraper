import requests
from bs4 import BeautifulSoup
import time
from scrapers.base_scraper import BaseScraper
from job import Job


class NHSScraper(BaseScraper):
    
    def __init__(self):
        super().__init__(
            company_name="NHS",
            base_url="https://www.jobs.nhs.uk/candidate/search/results"
        )
    
    def scrape_jobs(self, search_term="software engineering"):
        jobs_list = []
        page = 1
        
        while True:    
            params = {
                "keyword": search_term,
                "language": "en",
                "page": page
            }
            
            response = requests.get(self.base_url, params=params) 
            if response.status_code != 200:
                break
            
            soup = BeautifulSoup(response.text, "html.parser")
            jobs = soup.find_all("li", {"data-test": "search-result"})
            
            if not jobs:
                break
            
            for job in jobs:      
                job_object = self.parse_job(job)
                jobs_list.append(job_object)
                         
            page += 1
            time.sleep(self.delay)
        
        return jobs_list
    
    def parse_job(self, job):
        title = job.find("a", {"data-test": "search-result-job-title"}).text.strip()
        link = job.find("a", {"data-test": "search-result-job-title"})["href"]
        url = f"https://www.jobs.nhs.uk{link}"
        
        job_object = Job(self.company_name, title, url=url)
        
        return job_object


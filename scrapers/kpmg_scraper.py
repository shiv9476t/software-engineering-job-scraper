import requests
from bs4 import BeautifulSoup
import time
from scrapers.base_scraper import BaseScraper
from job import Job


class KPMGScraper(BaseScraper):
    
    def __init__(self):
        super().__init__(
            company_name="KPMG",
            base_url="https://www.kpmgcareers.co.uk/search/vacancies/"
        )
    
    def scrape_jobs(self, search_term="software engineering"):
        jobs_list = []
        page = 1
        
        while True:
            params = {
                "searchText": search_term,
                "page": page
            }
            
            response = requests.get(self.base_url, params=params)
            if response.status_code != 200:
                break
            
            soup = BeautifulSoup(response.text, "html.parser")
            jobs = soup.find_all("div", class_="vacancy-result")
            
            if not jobs:
                break
            
            for job in jobs:
                job_object = self.parse_job(job)
                if job_object:
                    jobs_list.append(job_object)
                        
            page += 1
            time.sleep(self.delay)
        
        return jobs_list
    
    def parse_job(self, job):
        title = job.find("h3").text.strip()
        link_tag = job.find("a", class_="view-job-description")        
        link = "https://www.kpmgcareers.co.uk" + link_tag["href"]
                
        job_object = Job(self.company_name, title, url=link)
        
        return job_object
        


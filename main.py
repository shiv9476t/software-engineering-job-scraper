from scrapers.kpmg_scraper import KPMGScraper
from scrapers.lloyds_scraper import LloydsScraper
from scrapers.nhs_scraper import NHSScraper
from database.job_database import JobDatabase

job_database = JobDatabase()
scrapers = [KPMGScraper(), LloydsScraper(), NHSScraper()]

for scraper in scrapers:
    jobs = scraper.scrape_jobs()
    for job in jobs:
        job_database.save_job(job)
        
job_database.close()



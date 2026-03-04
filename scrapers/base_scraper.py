class BaseScraper:
    
    def __init__(self, company_name, base_url, delay=1):
        self.company_name = company_name
        self.base_url = base_url
        self.delay = delay
    
    def scrape_jobs(self):
        raise NotImplementedError
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from webscraping.items import DataItem 

class CFASpider(scrapy.Spider):
    name = 'cfaspider'
        
    def start_requests(self):
        url = 'https://www.cfainstitute.org/en/membership/professional-development/refresher-readings#sort=%40refreadingcurriculumyear%20descending'
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        count = 0
        while True:
            count += 1
            time.sleep(3)
            # Extracting links with class name 'CoveoResultLink'
            links = driver.find_elements(By.CSS_SELECTOR, "a.CoveoResultLink")
            # Extract and print the href attribute of each link
            for linkTag in links:
                href = linkTag.get_attribute("href")
                yield scrapy.Request(href)
            
            # If button available click and go to next page else break
            try:
                nextButton = driver.find_element(By.CSS_SELECTOR, "a[title='Next']")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(0.5)
                nextButton.click()
            except:
                print("Done scraping")
                break

    def parse(self, response):
        title = response.css('h1.article-title::text').get()
        year = self.tryOptional(lambda: re.sub(r'[\n\r]', '', response.css('span.content-utility-curriculum::text').get()).strip().split()[0]) 
        program = re.sub(r'[\'"‘’”“\n\r]', '', response.css('span.content-utility-level::text').get()).strip()
        level = re.sub(r'[\'"‘’”“\n\r]', '', response.css('span.content-utility-topic::text').get()).strip()
        program_level = program + ' ' + level
        
        # extract introduction
        introduction = self.tryOptional(self.extract_introduction, response)

        # extract learning outcomes
        learning_section = self.tryOptional(self.extract_learningOutcomes, response)
        
        # extract summary
        summary_section = self.tryOptional(self.extract_summary, response)
        
        # extract pdf link
        pdf_link = self.tryOptional(self.extract_pdflink, response)
        
        data_item = DataItem(
            topic = title,
            year = year,
            level = program_level,
            introduction = introduction,
            learning_outcomes = learning_section,
            summary = summary_section,
            link_summary = response.url,
            link_pdf = pdf_link
        )
        yield data_item

    def tryOptional(self, callableBlock, *args):
        try:
            result = callableBlock(*args)
            return result
        except:
            return None
        
    def extract_introduction(self, response):
        # Fetch intro section
        intro_section = response.css("h2:contains('Introduction')").xpath('..')
        # Remove the header from intro section
        intro_section.css('h2.article-section').remove()
        # Removing all html tags, new lines and carriage returns
        introduction = re.sub(r'[\'"‘’”“]|<.*?>', '', intro_section.get()).strip('\r\n ')
        introduction = re.sub(r'\s+', ' ', introduction)
        return introduction
    
    def extract_learningOutcomes(self, response):
        # Fetch learning outcomes section
        h2tag_learningOutcomes = response.css('h2:contains("Learning Outcomes")')
        # Fetching the section below learning outcomes
        learning_section = h2tag_learningOutcomes.xpath('following-sibling::section[1]').get()
        # Removing all html tags, new lines and carriage returns
        learning_section = re.sub(r'[\'"‘’”“]|<.*?>', '', learning_section).strip('\r\n ')
        learning_section = re.sub(r'\s+', ' ', learning_section)
        return learning_section
    
    def extract_summary(self, response):
        # Fetch summary section
        h2tag_summary = response.css('h2:contains("Summary")')
        # Fetching the section below summary
        summary_section = h2tag_summary.xpath('following-sibling::div').get()
        # Removing all html tags, new lines and carriage returns
        summary_section = re.sub(r'[\'"‘’”“\n\r]|<.*?>', '', summary_section).strip('\r\n ')
        summary_section = re.sub(r'\s+', ' ', summary_section)
        return summary_section
    
    def extract_pdflink(self, response):
        base_url = 'https://www.cfainstitute.org'
        pdf_link = ''
        # Extracting pdf download links
        locked_href_links = response.css('a.locked-content::attr(href)').getall()
        for link in locked_href_links:
            if '.pdf' in link:
                pdf_link = base_url + link
        return pdf_link
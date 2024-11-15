#scrape.py
import selenium.webdriver as webdriver
import selenium.webdriver.chrome.service as service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_website(website):
    logger.info(f"Loading website: {website}")
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service.Service(chrome_driver_path), options=options)
    try:
        driver.get(website)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logger.info("Website loaded successfully.")
        return driver.page_source
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    cleaned_content = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)]

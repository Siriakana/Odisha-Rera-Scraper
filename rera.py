from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def configure_chrome_options():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Enable this for headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return chrome_options

def get_project_details(driver, project_url):
    details = {
        'Promoter Name': 'N/A',
        'Address': 'N/A',
        'GST No': 'N/A'
    }

    try:
        driver.get(project_url)

        # Click the "Promoter Details" tab
        tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Promoter Details')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", tab)
        tab.click()

        # Wait for the elements to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lblCompanyName")))

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        promoter_name = soup.find("span", id="lblCompanyName")
        promoter_address = soup.find("span", id="lblCompanyAddress")
        gst_no = soup.find("span", id="lblGST")

        if promoter_name:
            details['Promoter Name'] = promoter_name.get_text(strip=True)
        if promoter_address:
            details['Address'] = promoter_address.get_text(strip=True)
        if gst_no:
            details['GST No'] = gst_no.get_text(strip=True)

    except Exception as e:
        print(f"Error scraping {project_url}: {str(e)}")

    return details

def scrape_rera_projects():
    base_url = "https://rera.odisha.gov.in"
    list_url = f"{base_url}/projects/project-list"

    projects = []
    driver = None

    try:
        chrome_options = configure_chrome_options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print("Loading project list page...")
        driver.get(list_url)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table')

        if not table:
            raise ValueError("Could not find project table.")

        rows = table.find_all('tr')[1:7]  # First 6 rows (excluding header)

        print(f"Found {len(rows)} projects. Scraping details...")

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                rera_no = cols[0].get_text(strip=True)
                project_name = cols[1].get_text(strip=True)
                link = cols[1].find('a')

                if link and 'href' in link.attrs:
                    project_url = f"{base_url}{link['href']}"
                    print(f"\nScraping: {project_name}")
                    details = get_project_details(driver, project_url)

                    projects.append({
                        'Rera Regd. No': rera_no,
                        'Project Name': project_name,
                        **details,
                        'Project URL': project_url
                    })

                    time.sleep(4)

    except Exception as e:
        print(f"\nError in main scraping function: {str(e)}")
        if driver:
            driver.save_screenshot('error_screenshot.png')
            print("Saved screenshot as error_screenshot.png")
    finally:
        if driver:
            driver.quit()

    return projects

def save_to_csv(data, filename='rera_projects.csv'):
    if not data:
        print("No data to save")
        return

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\nData saved to {filename}")

if __name__ == "__main__":
    print("Starting Odisha RERA project scraper...")
    start_time = time.time()

    project_data = scrape_rera_projects()

    if project_data:
        print("\nSuccessfully scraped projects:")
        for i, project in enumerate(project_data, 1):
            print(f"\nProject {i}:")
            print(f"Rera No: {project['Rera Regd. No']}")
            print(f"Name: {project['Project Name']}")
            print(f"Promoter: {project['Promoter Name']}")
            print(f"Address: {project['Address']}")
            print(f"GST No: {project['GST No']}")

        save_to_csv(project_data)
    else:
        print("\nFailed to scrape projects. Please check the site or your setup.")

    print(f"\nExecution time: {time.time() - start_time:.2f} seconds")

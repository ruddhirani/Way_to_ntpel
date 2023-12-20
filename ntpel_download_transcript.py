import time
import argparse
import urllib.request as url
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

class CourseTranscriptDownloader:
    def __init__(self, course_url, driver_directory, output_path):
        """
        Initializes the CourseTranscriptDownloader.

        Args:
            course_url (str): URL of the course website.
            driver_directory (str): Path to the driver directory.
            output_path (str): Path to the output folder to store the PDF files.
        """
        self.course_url = course_url
        self.driver_directory = driver_directory
        self.output_path = output_path
        self.driver = None

    def download_transcripts(self):
        """
        Downloads the transcripts from the course website.
        """
        self.initialize_driver()
        self.navigate_to_website()
        self.click_view_transcripts()
        chapter_names = self.get_chapter_names()
        self.download_pdf_transcripts(chapter_names)
        self.close_driver()

    def initialize_driver(self):
        """
        Initializes the Chrome driver.
        """
        self.driver = webdriver.Chrome(service=Service(executable_path=self.driver_directory))

    def navigate_to_website(self):
        """
        Navigates to the course website.
        """
        self.driver.get(self.course_url)
        self.driver.maximize_window()
        time.sleep(5)

    def click_view_transcripts(self):
        """
        Clicks the "Downloads" button and then the "View Transcripts" button.
        """
        download_button = self.driver.find_element(By.XPATH, "//span[@class='tab']")
        download_button.click()
        time.sleep(2)

        view_transcripts_button = self.driver.find_element(By.XPATH,
                                                           "/html/body/app-root/app-course-details/main/section/app-course-detail-ui/div/div[3]/app-course-downloads/div/div[2]/div[1]/h3[1]")
        view_transcripts_button.click()
        time.sleep(2)

    def get_chapter_names(self):
        """
        Retrieves the chapter names from the course website.

        Returns:
            list: A list of chapter names.
        """
        chapter_list = self.driver.find_elements(By.CLASS_NAME, "c-name")
        chapter_count = len(chapter_list)
        chapter_names = []

        for i in range(chapter_count - 1):
            language_button = self.driver.find_element(By.XPATH,
                                                       f"/html/body/app-root/app-course-details/main/section/app-course-detail-ui/div/div[3]/app-course-downloads/div/div[2]/div[2]/div[{i + 2}]/div[1]/app-nptel-dropdown/div/span")
            language_button.click()
            time.sleep(2)

            english_button = self.driver.find_element(By.XPATH,
                                                      f"/html/body/app-root/app-course-details/main/section/app-course-detail-ui/div/div[3]/app-course-downloads/div/div[2]/div[2]/div[{i + 2}]/div[1]/app-nptel-dropdown/ul/li")
            self.driver.execute_script("arguments[0].scrollIntoView();", english_button)
            time.sleep(0.5)

            self.driver.execute_script("arguments[0].click();", english_button)

            chapter_names.append(chapter_list[i + 1].text)

        return chapter_names

    def download_pdf_transcripts(self, chapter_names):
        """
        Downloads the PDF transcripts for each chapter.

        Args:
            chapter_names (list): List of chapter names.
        """
        drive_links = self.driver.find_elements(By.XPATH, "//a[contains(@href,'drive.google.com')]")
        pdf_links = [link.get_attribute("href") for link in drive_links]

        chapter_name = 1
        for i in range(len(pdf_links) - 1):
            link = pdf_links[i]
            filename = link.split('/')[5]
            download_url = f"https://drive.google.com/uc?id={filename}&export=download"
            output_filename = f'{self.output_path}/lectures_{chapter_name}.pdf'
            print(output_filename)
            url.urlretrieve(download_url, output_filename)
            chapter_name += 1

    def close_driver(self):
        """
        Closes the Chrome driver.
        """
        self.driver.quit()


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Downloaded pdf transcript files from given URL")
    parser.add_argument('--course_url', required=True, help='URL of the required website to access')
    parser.add_argument('--driver_directory', required=True, help='Path to the driver directory')
    parser.add_argument('--output_path', required=True, help='Path to the output folder to store the pdf files')
    args = parser.parse_args()

    # Initialize and run the downloader
    course_downloader = CourseTranscriptDownloader(args.course_url, args.driver_directory, args.output_path)
    course_downloader.download_transcripts()


if __name__ == "__main__":
    main()


"""Finds 'n' properties within the circle.

Args:
    properties (list): List of property objects.
    n (int): Number of properties to find.

Returns:
    PropertyResult: List of property data.
"""

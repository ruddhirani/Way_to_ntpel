import yt_dlp
import time
import argparse
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class CourseDownloader:
    def __init__(self, course_url, driver_directory, output_path):
        """
        Initializes the CourseDownloader.

        Args:
            course_url (str): URL of the course website.
            driver_directory (str): Path to the driver directory.
            output_path (str): Path to the output folder to store the MP3 files.
        """
        self.course_url = course_url
        self.driver_directory = driver_directory
        self.output_path = output_path
        self.driver = None
        self.video_links = []

    def download_course(self):
        """
        Downloads the course lectures.
        """
        self.initialize_driver()
        self.navigate_to_website()
        self.get_video_links()
        self.download_videos()
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
        time.sleep(5)  # Wait for the website to load

    def get_video_links(self):
        """
        Retrieves the video links for each week and lesson.
        """
        week_list = self.driver.find_elements(By.CLASS_NAME, "unit-title")
        live_list = self.driver.find_elements(By.LINK_TEXT, "Live Session")
        week_count = len(week_list) - len(live_list)

        for week in range(week_count - 1):
            time.sleep(4)  # Wait for the content to load
            week_button = self.driver.find_element(By.XPATH, f"/html/body/app-root/app-course-details/main/nav/div/div[{week + 2}]/div/span")
            week_button.click()  # Click the week button

            lesson_list = self.driver.find_elements(By.XPATH, "//div[@class='unit selected']//ul[@class='lessons-list']//li[@class='lesson']")
            lesson_count = len(lesson_list)

            for lesson in range(lesson_count + 1):
                lesson_button = self.driver.find_element(By.XPATH, f"/html/body/app-root/app-course-details/main/nav/div/div[{week + 2}]/ul/li[{lesson + 1}]/span")
                lesson_button.click()  # Click the lesson button
                time.sleep(2)  # Wait for the content to load

                frame = self.driver.find_element(By.ID, "player")
                self.driver.switch_to.frame(frame)  # Switch to the video frame

                youtube_link = self.driver.find_element(By.XPATH, "//a[@data-layer='8']")
                youtube_href = youtube_link.get_attribute('href')
                video_link = youtube_href.split('&')[0]  # Extract the video link from the href attribute
                self.video_links.append(video_link)  # Add the video link to the list

                self.driver.switch_to.default_content()  # Switch back to the main frame

            self.driver.get(self.course_url)  # Navigate back to the main course page

    def download_videos(self):
        """
        Downloads the videos from the video links.
        """
        for i, link in tqdm(enumerate(self.video_links, start=1)):
            file_name = "lecture_" + str(i)
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': self.output_path + '/' + file_name
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

    def close_driver(self):
        """
        Closes the Chrome driver.
        """
        self.driver.quit()


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Download MP3 lecture files from a given URL")
    parser.add_argument('--course_url', required=True, help='URL of the required website to access')
    parser.add_argument('--driver_directory', required=True, help='Path to the driver directory')
    parser.add_argument('--output_path', required=True, help='Path to the output folder to store the MP3 files')
    args = parser.parse_args()

    # Create a CourseDownloader instance and initiate the download
    course_downloader = CourseDownloader(args.course_url, args.driver_directory, args.output_path)
    course_downloader.download_course()


if __name__ == "__main__":
    main()


"""Finds 'n' properties within the circle.

Args:
    properties (list): List of property objects.
    n (int): Number of properties to find.

Returns:
    PropertyResult: List of property data.
"""

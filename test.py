import unittest
from threading import Thread
import os
from models import Apartment
from Question6 import Scraping, scrape_divar

class TestScraping(unittest.TestCase):
    def test_get_advertisement_success(self):
        divar = Scraping(targetURL="https://divar.ir/s/tehran/buy-residential")
        result = divar.get_advertisement()
        self.assertIsNotNone(result)
        self.assertEqual(result.status_code, 200)

    def test_get_advertisement_failure(self):
        divar = Scraping(targetURL="https://invalid-url.com")
        result = divar.get_advertisement()
        self.assertIsNone(result)

    def test_extraction_advertisement(self):
        divar = Scraping(targetURL="https://divar.ir/s/tehran/buy-residential")
        html_content = '<h2 class="kt-post-card__title">Title</h2><div class="kt-post-card__description">Price</div><a class="" href="/link">'
        divar.extraction_advertisement(html_content)
        self.assertEqual(divar.apartments[0].title, "Title")
        self.assertEqual(divar.apartments[0].price, "Price")
        self.assertEqual(divar.apartments[0].link, "https://divar.ir/link")

    def test_save_to_file(self):
        divar = Scraping(targetURL="https://divar.ir/s/tehran/buy-residential")
        divar.apartments = [Apartment("Title1", "Price1", "Link1"), Apartment("Title2", "Price2", "Link2")]
        file_path = "ScrapDivar.txt"
        divar.save_to_file(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        expected_content = "Title: Title1\nPrice: Price1\nLink: Link1\n\nTitle: Title2\nPrice: Price2\nLink: Link2\n\n"
        self.assertEqual(content, expected_content)

        os.remove(file_path)  # Clean up the test file

    def test_delete_file(self):
        file_path = "ScrapDivar.txt"
        with open(file_path, 'w') as file:
            file.write("Test Content")
        divar = Scraping(targetURL="https://divar.ir/s/tehran/buy-residential")
        divar.delete_file(file_path)
        self.assertFalse(os.path.exists(file_path))

    def test_scrape_divar(self):
        target_url = "https://divar.ir/s/tehran/buy-residential"
        file_path = "ScrapDivar.txt"
        scrape_divar(target_url, file_path)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)  # Clean up the test file

if __name__ == '__main__':
    unittest.main()

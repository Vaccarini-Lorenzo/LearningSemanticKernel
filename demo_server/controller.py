from esselunga_receipt_scraper.scraper import Scraper
import threading


class Controller:
    def __init__(self):
        self.scraper = Scraper(True)

    def start_scrape(self, data_storage):
        print("Running process - Contacting esselunga")
        self.scraper.authenticate()
        receipts_data = self.scraper.scrape_receipts()
        data_storage.update_storage(receipts_data)
        print(f"Updated data storage - {receipts_data}")
        self.scraper.clean()

    def schedule_function(self, function, time_sec, *args, **kwargs):
        function(*args, **kwargs)
        #threading.Timer(time_sec, self.schedule_function, [function, time_sec, *args], kwargs).start()

    def start_scheduling(self, data_storage):
        self.schedule_function(self.start_scrape, 1000, data_storage)
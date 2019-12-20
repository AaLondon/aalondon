from django.core.management.base import BaseCommand
from scraper.spiders.meeting_spider import AASpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(AASpider)
        process.start()
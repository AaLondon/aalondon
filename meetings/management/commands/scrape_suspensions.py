from django.core.management.base import BaseCommand
from scrapy.utils.project import get_project_settings
from multiprocessing import Process, Queue
from pcndodger.suspensions.spiders import MySpider
from twisted.internet import reactor
import scrapy.crawler as crawler


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        def f(q):
            try:
                print('A')
                runner = crawler.CrawlerRunner(get_project_settings())
                print('B')
                deferred = runner.crawl(MySpider)
                print('C')
                deferred.addBoth(lambda _: reactor.stop())
                print('D')
                reactor.run()
                print('E')
                q.put(None)
                print('F')
            except Exception as e:
                print('THIS IS AN EXCEPTION MOFO')
                raise
                q.put(e)

        q = Queue()
        p = Process(target=f, args=(q,))
        p.start()
        result = q.get()
        p.join()

        if result is not None:
            raise result




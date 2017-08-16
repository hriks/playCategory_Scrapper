from . import scraper


def details(app_id):
    s = scraper.PlayScraper()
    return s.details(app_id)


def collection(collection, category=None, **kwargs):
    s = scraper.PlayScraper()
    return s.collection(collection, category, **kwargs)


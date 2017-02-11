"""Test spider."""


from arias.item_loader import dmoz_loader
from arias.items import dmoz
from arias.spiders import base


class DmozSpider(base.BaseSpider):
    """Dmoz test spider."""
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        """Parse the response."""
        self.log('Processing')
        for sel in response.xpath('//ul/li'):
            loader = dmoz_loader.DmozItemLoader(
                dmoz.DmozItem(), selector=sel, response=response)
            loader.add_xpath('title', 'a/text()')
            loader.add_xpath('link', 'a/@href')
            loader.add_xpath('desc', 'text()')
            itm = loader.load_item()
            yield itm

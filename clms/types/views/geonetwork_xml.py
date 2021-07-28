# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from datetime import datetime
from bs4 import BeautifulSoup


class GeoNetworkXMLView(BrowserView):
    def __call__(self):
        # Implement your own actions:
        return self.index()

    def dateFromIso(self, dateIso):
        return datetime.fromisoformat(dateIso).date()

    def htmlToText(self, htmlCode):
        soup = BeautifulSoup(htmlCode, features="lxml")
        return soup.get_text()

# -*- coding: utf-8 -*-
"""
Geonetwork xml view
"""
from Products.Five.browser import BrowserView
from datetime import datetime
from bs4 import BeautifulSoup


class GeoNetworkXMLView(BrowserView):
    """
    Geonetwork xml view
    """

    def __call__(self):
        return self.index()

    def dateFromIso(self, dateIso):
        """
        Get date from ISO format
        """
        return datetime.fromisoformat(dateIso).date()

    def htmlToText(self, htmlCode):
        """
        Convert html code to text
        """
        soup = BeautifulSoup(htmlCode, features="lxml")
        return soup.get_text()

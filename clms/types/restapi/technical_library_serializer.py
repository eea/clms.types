"""Custom serializer for TechnicalLibrary content type."""

from html import unescape
import re
from urllib.request import Request
from urllib.request import urlopen

from clms.types.content.technical_library import ITechnicalLibrary
from plone.restapi.serializer.dxcontent import SerializeToJson
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from plone.restapi.interfaces import IFieldSerializer

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None


@implementer(IFieldSerializer)
@adapter(ITechnicalLibrary, Interface)
class TechnicalLibrarySerializer(SerializeToJson):
    """Custom serializer for TechnicalLibrary content."""

    def _strip_html_fallback(self, html):
        """Fallback text extraction using regex-based tag stripping."""
        html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
        html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)
        text = re.sub(r"(?is)<[^>]+>", " ", html)
        text = unescape(text)
        return re.sub(r"\s+", " ", text).strip()

    def _strip_html(self, html):
        """Preferred HTML-to-text extraction with fallback."""
        if BeautifulSoup is not None:
            try:
                soup = BeautifulSoup(html, "html.parser")
                for tag in soup(["script", "style", "noscript"]):
                    tag.decompose()
                text = soup.get_text(separator=" ", strip=True)
                text = unescape(text)
                return re.sub(r"\s+", " ", text).strip()
            except Exception:
                pass

        return self._strip_html_fallback(html)

    def _extract_external_text(self, url):
        """Fetch external page and return readable plain text."""
        request = Request(url, headers={"User-Agent": "clms-indexer/1.0"})
        with urlopen(request, timeout=15) as response:
            raw_body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"

        html = raw_body.decode(charset, errors="ignore")
        return self._strip_html(html)

    def __call__(self, version=None, include_items=True):
        result = super().__call__(version=version, include_items=include_items)

        request_form = getattr(self.request, "form", {}) or {}
        has_eea_index_flag = "eea_index" in request_form

        external_source_url = result.get("external_source_url")
        if has_eea_index_flag and external_source_url:
            try:
                result["external_content_text"] = self._extract_external_text(
                    external_source_url
                )
            except Exception:
                # Never break content serialization
                result["external_content_text"] = ""

        return result

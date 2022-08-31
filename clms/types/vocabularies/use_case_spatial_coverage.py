# -*- coding: utf-8 -*-
"""
Topics vocabulary definition
"""

from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


class VocabItem:
    """
    VocabItem class
    """

    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class UseCaseSpatialCoverageVocabulary:
    """
    Topics vocabulary class
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem("AD", "Andorra"),  # Disable?
            VocabItem("AE", "United Arab Emirates"),  # Disable?
            VocabItem("AF", "Afghanistan"),  # Disable?
            VocabItem("AG", "Antigua and Barbuda"),  # Disable?
            VocabItem("AI", "Anguilla"),  # Disable?
            VocabItem("AL", "Albania"),
            VocabItem("AM", "Armenia"),  # Disable?
            VocabItem("AO", "Angola"),  # Disable?
            VocabItem("AR", "Argentina"),  # Disable?
            VocabItem("AS", "American Samoa"),  # Disable?
            VocabItem("AT", "Austria"),
            VocabItem("BW", "Botswana"),  # Disable?
            VocabItem("CG", "Congo"),  # Disable?
            VocabItem("CH", "Switzerland"),
            VocabItem("CI", "Côte D’Ivoire"),  # Disable?
            VocabItem("CK", "Cook Islands"),  # Disable?
            VocabItem("AQ", "Antarctica"),  # Disable?
            VocabItem("BY", "Belarus"),  # Disable?
            VocabItem("BZ", "Belize"),  # Disable?
            VocabItem("BJ", "Benin"),  # Disable?
            VocabItem("BN", "Brunei"),  # Disable?
            VocabItem("BO", "Bolivia"),  # Disable?
            VocabItem("BQ", "Bonaire, Sint Eustatius and Saba"),  # Disable?
            VocabItem("BT", "Bhutan"),  # Disable?
            VocabItem("BV", "Bouvet Island"),  # Disable?
            VocabItem("BR", "Brazil"),  # Disable?
            VocabItem("BS", "Bahamas"),  # Disable?
            VocabItem("CA", "Canada"),  # Disable?
            VocabItem("AU", "Australia"),  # Disable?
            VocabItem("AW", "Aruba"),  # Disable?
            VocabItem("AZ", "Azerbaijan"),  # Disable?
            VocabItem("BA", "Bosnia and Herzegovina"),
            VocabItem("BB", "Barbados"),  # Disable?
            VocabItem("BD", "Bangladesh"),  # Disable?
            VocabItem("BE", "Belgium"),
            VocabItem("BF", "Burkina Faso"),  # Disable?
            VocabItem("BG", "Bulgaria"),
            VocabItem("BH", "Bahrain"),  # Disable?
            VocabItem("BI", "Burundi"),  # Disable?
            VocabItem("CL", "Chile"),  # Disable?
            VocabItem("CD", "Democratic Republic of The Congo"),  # Disable?
            VocabItem("CF", "Central African Republic"),  # Disable?
            VocabItem("CN", "China"),  # Disable?
            VocabItem("DJ", "Djibouti"),  # Disable?
            VocabItem("DM", "Dominica"),  # Disable?
            VocabItem("DO", "Dominican Republic"),  # Disable?
            VocabItem("CO", "Colombia"),  # Disable?
            VocabItem("CR", "Costa Rica"),  # Disable?
            VocabItem("CU", "Cuba"),  # Disable?
            VocabItem("CV", "Cape Verde"),  # Disable?
            VocabItem("CW", "Curaçao"),  # Disable?
            VocabItem("CY", "Cyprus"),
            VocabItem("CZ", "Czechia"),
            VocabItem("FI", "Finland"),
            VocabItem("CM", "Cameroon"),  # Disable?
            VocabItem("DE", "Germany"),
            VocabItem("DZ", "Algeria"),  # Disable?
            VocabItem("DK", "Denmark"),
            VocabItem("ER", "Eritrea"),  # Disable?
            VocabItem("EL", "Greece"),
            VocabItem("ET", "Ethiopia"),  # Disable?
            VocabItem("FM", "Micronesia"),  # Disable?
            VocabItem("FO", "Faroes"),  # Disable?
            VocabItem("GA", "Gabon"),  # Disable?
            VocabItem("GD", "Grenada"),  # Disable?
            VocabItem("GE", "Georgia"),  # Disable?
            VocabItem("GG", "Guernsey"),  # Disable?
            VocabItem("GH", "Ghana"),  # Disable?
            VocabItem("GI", "Gibraltar"),  # Disable?
            VocabItem("FR", "France"),
            VocabItem("ES", "Spain"),
            VocabItem("FJ", "Fiji"),  # Disable?
            VocabItem("FK", "Falkland Islands"),  # Disable?
            VocabItem("EC", "Ecuador"),  # Disable?
            VocabItem("EE", "Estonia"),
            VocabItem("EG", "Egypt"),  # Disable?
            VocabItem("EH", "Western Sahara"),  # Disable?
            VocabItem("GL", "Greenland"),  # Disable?
            VocabItem("GM", "Gambia"),  # Disable?
            VocabItem("GN", "Guinea"),  # Disable?
            VocabItem("GQ", "Equatorial Guinea"),  # Disable?
            VocabItem(
                "GS", "South Georgia and The South Sandwich Islands"
            ),  # Disable?
            VocabItem("GT", "Guatemala"),  # Disable?
            VocabItem("GU", "Guam"),  # Disable?
            VocabItem("GW", "Guinea-Bissau"),  # Disable?
            VocabItem("HR", "Croatia"),
            VocabItem("HT", "Haiti"),  # Disable?
            VocabItem("HU", "Hungary"),
            VocabItem("GY", "Guyana"),  # Disable?
            VocabItem("HK", "Hong Kong"),  # Disable?
            VocabItem("HM", "Heard Island and Mcdonald Islands"),  # Disable?
            VocabItem("HN", "Honduras"),  # Disable?
            VocabItem("KH", "Cambodia"),  # Disable?
            VocabItem("KI", "Kiribati"),  # Disable?
            VocabItem("KM", "Comoros"),  # Disable?
            VocabItem("KN", "Saint Kitts and Nevis"),  # Disable?
            VocabItem("KP", "North Korea"),  # Disable?
            VocabItem("KW", "Kuwait"),  # Disable?
            VocabItem("KY", "Cayman Islands"),  # Disable?
            VocabItem("NP", "Nepal"),  # Disable?
            VocabItem("NR", "Nauru"),  # Disable?
            VocabItem("NU", "Niue"),  # Disable?
            VocabItem("IT", "Italy"),
            VocabItem("LC", "Saint Lucia"),  # Disable?
            VocabItem("LI", "Liechtenstein"),
            VocabItem("MR", "Mauritania"),  # Disable?
            VocabItem("KR", "South Korea"),  # Disable?
            VocabItem("LA", "Laos"),  # Disable?
            VocabItem("MS", "Montserrat"),  # Disable?
            VocabItem("JP", "Japan"),  # Disable?
            VocabItem("KG", "Kyrgyzstan"),  # Disable?
            VocabItem("ID", "Indonesia"),  # Disable?
            VocabItem("IE", "Ireland"),
            VocabItem("IL", "Israel"),  # Disable?
            VocabItem("IM", "Isle of Man"),  # Disable?
            VocabItem("IO", "British Indian Ocean Territory"),  # Disable?
            VocabItem("IN", "India"),  # Disable?
            VocabItem("IQ", "Iraq"),  # Disable?
            VocabItem("IS", "Iceland"),
            VocabItem("JE", "Jersey"),  # Disable?
            VocabItem("JM", "Jamaica"),  # Disable?
            VocabItem("JO", "Jordan"),  # Disable?
            VocabItem("IR", "Iran"),  # Disable?
            VocabItem("KE", "Kenya"),  # Disable?
            VocabItem("OM", "Oman"),  # Disable?
            VocabItem("LB", "Lebanon"),  # Disable?
            VocabItem("LS", "Lesotho"),  # Disable?
            VocabItem("LT", "Lithuania"),
            VocabItem("LU", "Luxembourg"),
            VocabItem("LV", "Latvia"),
            VocabItem("LY", "Libya"),  # Disable?
            VocabItem("MA", "Morocco"),  # Disable?
            VocabItem("MM", "Myanmar/Burma"),  # Disable?
            VocabItem("NO", "Norway"),
            VocabItem("PA", "Panama"),  # Disable?
            VocabItem("LK", "Sri Lanka"),  # Disable?
            VocabItem("LR", "Liberia"),  # Disable?
            VocabItem("ML", "Mali"),  # Disable?
            VocabItem("MN", "Mongolia"),  # Disable?
            VocabItem("MO", "Macau"),  # Disable?
            VocabItem("MP", "Northern Mariana Islands"),  # Disable?
            VocabItem("NE", "Niger"),  # Disable?
            VocabItem("MD", "Moldova"),  # Disable?
            VocabItem("ME", "Montenegro"),
            VocabItem("MG", "Madagascar"),  # Disable?
            VocabItem("MK", "North Macedonia"),
            VocabItem("MT", "Malta"),
            VocabItem("MU", "Mauritius"),  # Disable?
            VocabItem("KZ", "Kazakhstan"),  # Disable?
            VocabItem("MW", "Malawi"),  # Disable?
            VocabItem("MY", "Malaysia"),  # Disable?
            VocabItem("MZ", "Mozambique"),  # Disable?
            VocabItem("NA", "Namibia"),  # Disable?
            VocabItem("NC", "New Caledonia"),  # Disable?
            VocabItem("NG", "Nigeria"),  # Disable?
            VocabItem("NI", "Nicaragua"),  # Disable?
            VocabItem("NL", "Netherlands"),
            VocabItem("PG", "Papua New Guinea"),  # Disable?
            VocabItem("PT", "Portugal"),
            VocabItem("PW", "Palau"),  # Disable?
            VocabItem("PY", "Paraguay"),  # Disable?
            VocabItem("QA", "Qatar"),  # Disable?
            VocabItem("RO", "Romania"),
            VocabItem("NZ", "New Zealand"),  # Disable?
            VocabItem("PE", "Peru"),  # Disable?
            VocabItem("PF", "French Polynesia"),  # Disable?
            VocabItem("NF", "Norfolk Island"),  # Disable?
            VocabItem("MX", "Mexico"),  # Disable?
            VocabItem("PH", "Philippines"),  # Disable?
            VocabItem("PK", "Pakistan"),  # Disable?
            VocabItem("PL", "Poland"),
            VocabItem("PM", "Saint Pierre and Miquelon"),  # Disable?
            VocabItem("PN", "Pitcairn Islands"),  # Disable?
            VocabItem("PR", "Puerto Rico"),  # Disable?
            VocabItem("PS", "Palestine"),  # Disable?
            VocabItem("RS", "Serbia"),
            VocabItem("RU", "Russian Federation"),  # Disable?
            VocabItem("RW", "Rwanda"),  # Disable?
            VocabItem("SA", "Saudi Arabia"),  # Disable?
            VocabItem("TF", "French Southern and Antarctic Lands"),  # Disable?
            VocabItem("TG", "Togo"),  # Disable?
            VocabItem("TH", "Thailand"),  # Disable?
            VocabItem("TJ", "Tajikistan"),  # Disable?
            VocabItem("TL", "Timor-Leste"),  # Disable?
            VocabItem("SS", "South Sudan"),  # Disable?
            VocabItem("ST", "São Tomé and Príncipe"),  # Disable?
            VocabItem("SV", "El Salvador"),  # Disable?
            VocabItem("SY", "Syria"),  # Disable?
            VocabItem("SZ", "Eswatini"),  # Disable?
            VocabItem("TC", "Turks and Caicos Islands"),  # Disable?
            VocabItem("TD", "Chad"),  # Disable?
            VocabItem("SC", "Seychelles"),  # Disable?
            VocabItem("SB", "Solomon Islands"),  # Disable?
            VocabItem("TT", "Trinidad and Tobago"),  # Disable?
            VocabItem("TR", "Turkey"),
            VocabItem("TZ", "United Republic of Tanzania"),  # Disable?
            VocabItem("SD", "Sudan"),  # Disable?
            VocabItem("SE", "Sweden"),
            VocabItem("SG", "Singapore"),  # Disable?
            VocabItem(
                "SH", "Saint Helena, Ascension and Tristan Da Cunha"
            ),  # Disable?
            VocabItem("SI", "Slovenia"),
            VocabItem("SK", "Slovakia"),
            VocabItem("SL", "Sierra Leone"),  # Disable?
            VocabItem("SM", "San Marino"),  # Disable?
            VocabItem("SN", "Senegal"),  # Disable?
            VocabItem("TM", "Turkmenistan"),  # Disable?
            VocabItem("TN", "Tunisia"),  # Disable?
            VocabItem("TO", "Tonga"),  # Disable?
            VocabItem("SO", "Somalia"),  # Disable?
            VocabItem("SR", "Suriname"),  # Disable?
            VocabItem("SJ", "Svalbard and Jan Mayen"),  # Disable?
            VocabItem("XV", "Bir Tawil (Disputed Territory)"),  # Disable?
            VocabItem("YE", "Yemen"),  # Disable?
            VocabItem("ZA", "South Africa"),  # Disable?
            VocabItem("ZM", "Zambia"),  # Disable?
            VocabItem("ZW", "Zimbabwe"),  # Disable?
            VocabItem("UA", "Ukraine"),  # Disable?
            VocabItem("UG", "Uganda"),  # Disable?
            VocabItem("UK", "United Kingdom"),
            VocabItem("XH", "Jammu Kashmir"),  # Disable?
            VocabItem("XI", "Kuril Islands"),  # Disable?
            VocabItem("XO", "Bassas Da India"),  # Disable?
            VocabItem("XU", "Abyei"),  # Disable?
            VocabItem("VE", "Venezuela"),  # Disable?
            VocabItem("VG", "British Virgin Islands"),  # Disable?
            VocabItem("VI", "Us Virgin Islands"),  # Disable?
            VocabItem("VU", "Vanuatu"),  # Disable?
            VocabItem("VN", "Vietnam"),  # Disable?
            VocabItem("WS", "Samoa"),  # Disable?
            VocabItem("XC", "Aksai Chin"),  # Disable?
            VocabItem("XD", "Arunachal Pradesh"),  # Disable?
            VocabItem("XE", "China/India"),  # Disable?
            VocabItem("XF", "Hala'Ib Triangle"),  # Disable?
            VocabItem("XG", "Ilemi Triangle"),  # Disable?
            VocabItem("US", "United States"),  # Disable?
            VocabItem("UY", "Uruguay"),  # Disable?
            VocabItem("UZ", "Uzbekistan"),  # Disable?
            VocabItem("VA", "Vatican City"),  # Disable?
            VocabItem("VC", "Saint Vincent and The Grenadines"),  # Disable?
            VocabItem("KO", "Kosovo under UNSCR 1244/99*)"),
            VocabItem("EEA", "European Environment Agency"),
            VocabItem("EU", "European Union"),
            VocabItem("EU 27+UK", "European Union + United Kingdom"),
        ]

        # create a list of SimpleTerm items:
        terms = []
        for item in sorted(items, key=lambda x: x.value):
            terms.append(
                SimpleTerm(
                    value=item.token,
                    token=str(item.token),
                    title=item.value,
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


UseCaseSpatialCoverageVocabularyFactory = UseCaseSpatialCoverageVocabulary()

import string

from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

# Dictionary of ISO country code to IBAN length.
#
# The official IBAN Registry document is the best source for up-to-date information about IBAN formats and which
# countries are in IBAN.
#
# https://www.swift.com/standards/data-standards/iban
#
# The IBAN_COUNTRY_CODE_LENGTH dictionary has been updated version 78 of the IBAN Registry document which was published
# in August 2017.
#
# Other Resources:
#
# https://en.wikipedia.org/wiki/International_Bank_Account_Number#IBAN_formats_by_country
# http://www.ecbs.org/iban/france-bank-account-number.html
# https://www.nordea.com/V%C3%A5ra+tj%C3%A4nster/Internationella+produkter+och+tj%C3%A4nster/Cash+Management/IBAN+countries/908472.html

IBAN_COUNTRY_CODE_LENGTH = {
    'AD': 24,  # Andorra
    'AE': 23,  # United Arab Emirates
    'AL': 28,  # Albania
    'AT': 20,  # Austria
    'AZ': 28,  # Azerbaijan
    'BA': 20,  # Bosnia and Herzegovina
    'BE': 16,  # Belgium
    'BG': 22,  # Bulgaria
    'BH': 22,  # Bahrain
    'BR': 29,  # Brazil
    'BY': 28,  # Republic of Belarus
    'CH': 21,  # Switzerland
    'CR': 22,  # Costa Rica
    'CY': 28,  # Cyprus
    'CZ': 24,  # Czech Republic
    'DE': 22,  # Germany
    'DK': 18,  # Denmark
    'DO': 28,  # Dominican Republic
    'EE': 20,  # Estonia
    'ES': 24,  # Spain
    'FI': 18,  # Finland
    'FO': 18,  # Faroe Islands
    'FR': 27,  # France + French Guiana (GF), Guadeloupe (GP), Martinique (MQ), Réunion (RE),
    #          French Polynesia (PF), French Southern Territories (TF), Mayotte (YT),
    #          New Caledonia (NC), Saint Barthélemy (BL),
    #          Saint Martin - French part (MF), Saint-Pierre and Miquelon (PM),
    #          Wallis and Futuna (WF)
    'GB': 22,  # United Kingdom + Guernsey (GG), Isle of Man (IM), Jersey (JE)
    'GE': 22,  # Georgia
    'GI': 23,  # Gibraltar
    'GL': 18,  # Greenland
    'GR': 27,  # Greece
    'GT': 28,  # Guatemala
    'HR': 21,  # Croatia
    'HU': 28,  # Hungary
    'IE': 22,  # Ireland
    'IL': 23,  # Israel
    'IQ': 23,  # Iraq
    'IS': 26,  # Iceland
    'IT': 27,  # Italy
    'JO': 30,  # Jordan
    'KW': 30,  # Kuwait
    'KZ': 20,  # Kazakhstan
    'LB': 28,  # Lebanon
    'LC': 32,  # Saint Lucia
    'LI': 21,  # Liechtenstein
    'LT': 20,  # Lithuania
    'LU': 20,  # Luxembourg
    'LV': 21,  # Latvia
    'MC': 27,  # Monaco
    'MD': 24,  # Moldova
    'ME': 22,  # Montenegro
    'MK': 19,  # Macedonia
    'MR': 27,  # Mauritania
    'MT': 31,  # Malta
    'MU': 30,  # Mauritius
    'NL': 18,  # Netherlands
    'NO': 15,  # Norway
    'PK': 24,  # Pakistan
    'PL': 28,  # Poland
    'PS': 29,  # Palestine
    'PT': 25,  # Portugal
    'QA': 29,  # Qatar
    'RO': 24,  # Romania
    'RS': 22,  # Serbia
    'SA': 24,  # Saudi Arabia
    'SC': 31,  # Seychelles
    'SE': 24,  # Sweden
    'SI': 19,  # Slovenia
    'SK': 24,  # Slovakia
    'SM': 27,  # San Marino
    'ST': 25,  # Sao Tome and Principe
    'SV': 28,  # El Salvador
    'TL': 23,  # Timor-Leste
    'TN': 24,  # Tunisia
    'TR': 26,  # Turkey
    'UA': 29,  # Ukraine
    'VA': 22,  # Vatican
    'VG': 24,  # British Virgin Islands
    'XK': 20
}  # Kosovo (user-assigned country code)

# Nordea has catalogued IBANs for some additional countries but they are not part of the office IBAN network yet.
#
# Reference:
# https://www.nordea.com/V%C3%A5ra+tj%C3%A4nster/Internationella+produkter+och+tj%C3%A4nster/Cash+Management/IBAN+countries/908472.html

NORDEA_COUNTRY_CODE_LENGTH = {
    'AO': 25,  # Angola
    'BJ': 28,  # Benin
    'BF': 27,  # Burkina Faso
    'BI': 16,  # Burundi
    'CI': 28,  # Ivory Coast
    'CG': 27,  # Congo
    'CM': 27,  # Cameroon
    'CV': 25,  # Cape Verde
    'DZ': 24,  # Algeria
    'EG': 27,  # Egypt
    'GA': 27,  # Gabon
    'IR': 26,  # Iran
    'MG': 27,  # Madagascar
    'ML': 28,  # Mali
    'MZ': 25,  # Mozambique
    'SN': 28
}  # Senegal

#: ISO 3166-1 country list.
#: Sourced from https://www.iso.org/obp/ui on 2014-11-08
ISO_3166_1_ALPHA2_COUNTRY_CODES = (
    'AD',  # Andorra
    'AE',  # United Arab Emirates
    'AF',  # Afghanistan
    'AG',  # Antigua and Barbuda
    'AI',  # Anguilla
    'AL',  # Albania
    'AM',  # Armenia
    'AO',  # Angola
    'AQ',  # Antarctica
    'AR',  # Argentina
    'AS',  # American Samoa
    'AT',  # Austria
    'AU',  # Australia
    'AW',  # Aruba
    'AX',  # Åland Islands
    'AZ',  # Azerbaijan
    'BA',  # Bosnia and Herzegovina
    'BB',  # Barbados
    'BD',  # Bangladesh
    'BE',  # Belgium
    'BF',  # Burkina Faso
    'BG',  # Bulgaria
    'BH',  # Bahrain
    'BI',  # Burundi
    'BJ',  # Benin
    'BL',  # Saint Barthélemy
    'BM',  # Bermuda
    'BN',  # Brunei Darussalam
    'BO',  # Bolivia, Plurinational State of
    'BQ',  # Bonaire, Sint Eustatius and Saba
    'BR',  # Brazil
    'BS',  # Bahamas
    'BT',  # Bhutan
    'BV',  # Bouvet Island
    'BW',  # Botswana
    'BY',  # Belarus
    'BZ',  # Belize
    'CA',  # Canada
    'CC',  # Cocos (Keeling) Islands
    'CD',  # Congo, the Democratic Republic of the
    'CF',  # Central African Republic
    'CG',  # Congo
    'CH',  # Switzerland
    'CI',  # Côte d'Ivoire
    'CK',  # Cook Islands
    'CL',  # Chile
    'CM',  # Cameroon
    'CN',  # China
    'CO',  # Colombia
    'CR',  # Costa Rica
    'CU',  # Cuba
    'CV',  # Cabo Verde
    'CW',  # Curaçao
    'CX',  # Christmas Island
    'CY',  # Cyprus
    'CZ',  # Czech Republic
    'DE',  # Germany
    'DJ',  # Djibouti
    'DK',  # Denmark
    'DM',  # Dominica
    'DO',  # Dominican Republic
    'DZ',  # Algeria
    'EC',  # Ecuador
    'EE',  # Estonia
    'EG',  # Egypt
    'EH',  # Western Sahara
    'ER',  # Eritrea
    'ES',  # Spain
    'ET',  # Ethiopia
    'FI',  # Finland
    'FJ',  # Fiji
    'FK',  # Falkland Islands (Malvinas)
    'FM',  # Micronesia, Federated States of
    'FO',  # Faroe Islands
    'FR',  # France
    'GA',  # Gabon
    'GB',  # United Kingdom
    'GD',  # Grenada
    'GE',  # Georgia
    'GF',  # French Guiana
    'GG',  # Guernsey
    'GH',  # Ghana
    'GI',  # Gibraltar
    'GL',  # Greenland
    'GM',  # Gambia
    'GN',  # Guinea
    'GP',  # Guadeloupe
    'GQ',  # Equatorial Guinea
    'GR',  # Greece
    'GS',  # South Georgia and the South Sandwich Islands
    'GT',  # Guatemala
    'GU',  # Guam
    'GW',  # Guinea-Bissau
    'GY',  # Guyana
    'HK',  # Hong Kong
    'HM',  # Heard Island and McDonald Islands
    'HN',  # Honduras
    'HR',  # Croatia
    'HT',  # Haiti
    'HU',  # Hungary
    'ID',  # Indonesia
    'IE',  # Ireland
    'IL',  # Israel
    'IM',  # Isle of Man
    'IN',  # India
    'IO',  # British Indian Ocean Territory
    'IQ',  # Iraq
    'IR',  # Iran, Islamic Republic of
    'IS',  # Iceland
    'IT',  # Italy
    'JE',  # Jersey
    'JM',  # Jamaica
    'JO',  # Jordan
    'JP',  # Japan
    'KE',  # Kenya
    'KG',  # Kyrgyzstan
    'KH',  # Cambodia
    'KI',  # Kiribati
    'KM',  # Comoros
    'KN',  # Saint Kitts and Nevis
    'KP',  # Korea, Democratic People's Republic of
    'KR',  # Korea, Republic of
    'KW',  # Kuwait
    'KY',  # Cayman Islands
    'KZ',  # Kazakhstan
    'LA',  # Lao People's Democratic Republic
    'LB',  # Lebanon
    'LC',  # Saint Lucia
    'LI',  # Liechtenstein
    'LK',  # Sri Lanka
    'LR',  # Liberia
    'LS',  # Lesotho
    'LT',  # Lithuania
    'LU',  # Luxembourg
    'LV',  # Latvia
    'LY',  # Libya
    'MA',  # Morocco
    'MC',  # Monaco
    'MD',  # Moldova, Republic of
    'ME',  # Montenegro
    'MF',  # Saint Martin (French part)
    'MG',  # Madagascar
    'MH',  # Marshall Islands
    'MK',  # Macedonia, the former Yugoslav Republic of
    'ML',  # Mali
    'MM',  # Myanmar
    'MN',  # Mongolia
    'MO',  # Macao
    'MP',  # Northern Mariana Islands
    'MQ',  # Martinique
    'MR',  # Mauritania
    'MS',  # Montserrat
    'MT',  # Malta
    'MU',  # Mauritius
    'MV',  # Maldives
    'MW',  # Malawi
    'MX',  # Mexico
    'MY',  # Malaysia
    'MZ',  # Mozambique
    'NA',  # Namibia
    'NC',  # New Caledonia
    'NE',  # Niger
    'NF',  # Norfolk Island
    'NG',  # Nigeria
    'NI',  # Nicaragua
    'NL',  # Netherlands
    'NO',  # Norway
    'NP',  # Nepal
    'NR',  # Nauru
    'NU',  # Niue
    'NZ',  # New Zealand
    'OM',  # Oman
    'PA',  # Panama
    'PE',  # Peru
    'PF',  # French Polynesia
    'PG',  # Papua New Guinea
    'PH',  # Philippines
    'PK',  # Pakistan
    'PL',  # Poland
    'PM',  # Saint Pierre and Miquelon
    'PN',  # Pitcairn
    'PR',  # Puerto Rico
    'PS',  # Palestine, State of
    'PT',  # Portugal
    'PW',  # Palau
    'PY',  # Paraguay
    'QA',  # Qatar
    'RE',  # Réunion
    'RO',  # Romania
    'RS',  # Serbia
    'RU',  # Russian Federation
    'RW',  # Rwanda
    'SA',  # Saudi Arabia
    'SB',  # Solomon Islands
    'SC',  # Seychelles
    'SD',  # Sudan
    'SE',  # Sweden
    'SG',  # Singapore
    'SH',  # Saint Helena, Ascension and Tristan da Cunha
    'SI',  # Slovenia
    'SJ',  # Svalbard and Jan Mayen
    'SK',  # Slovakia
    'SL',  # Sierra Leone
    'SM',  # San Marino
    'SN',  # Senegal
    'SO',  # Somalia
    'SR',  # Suriname
    'SS',  # South Sudan
    'ST',  # Sao Tome and Principe
    'SV',  # El Salvador
    'SX',  # Sint Maarten (Dutch part)
    'SY',  # Syrian Arab Republic
    'SZ',  # Swaziland
    'TC',  # Turks and Caicos Islands
    'TD',  # Chad
    'TF',  # French Southern Territories
    'TG',  # Togo
    'TH',  # Thailand
    'TJ',  # Tajikistan
    'TK',  # Tokelau
    'TL',  # Timor-Leste
    'TM',  # Turkmenistan
    'TN',  # Tunisia
    'TO',  # Tonga
    'TR',  # Turkey
    'TT',  # Trinidad and Tobago
    'TV',  # Tuvalu
    'TW',  # Taiwan, Province of China
    'TZ',  # Tanzania, United Republic of
    'UA',  # Ukraine
    'UG',  # Uganda
    'UM',  # United States Minor Outlying Islands
    'US',  # United States
    'UY',  # Uruguay
    'UZ',  # Uzbekistan
    'VA',  # Holy See (Vatican City State)
    'VC',  # Saint Vincent and the Grenadines
    'VE',  # Venezuela, Bolivarian Republic of
    'VG',  # Virgin Islands, British
    'VI',  # Virgin Islands, U.S.
    'VN',  # Viet Nam
    'VU',  # Vanuatu
    'WF',  # Wallis and Futuna
    'WS',  # Samoa
    'YE',  # Yemen
    'YT',  # Mayotte
    'ZA',  # South Africa
    'ZM',  # Zambia
    'ZW',  # Zimbabwe
    'XK',  # Republic of Kosovo (user-assigned country code)
)


@deconstructible
class IBANValidator:
    """A validator for International Bank Account Numbers (IBAN - ISO 13616-1:2007)."""

    def __init__(self, use_nordea_extensions=False, include_countries=None):
        self.use_nordea_extensions = use_nordea_extensions
        self.include_countries = include_countries

        self.validation_countries = IBAN_COUNTRY_CODE_LENGTH.copy()
        if self.use_nordea_extensions:
            self.validation_countries.update(NORDEA_COUNTRY_CODE_LENGTH)

        if self.include_countries:
            for country_code in self.include_countries:
                if country_code not in self.validation_countries:
                    msg = 'Explicitly requested country code %s is not ' \
                          'part of the configured IBAN validation set.' % country_code
                    raise ImproperlyConfigured(msg)

    def __eq__(self, other):
        return (
            self.use_nordea_extensions == other.use_nordea_extensions
            and self.include_countries == other.include_countries
        )

    @staticmethod
    def iban_checksum(value):
        """
        Returns check digits for an input IBAN number.
        Original checksum in input value is ignored.
        """
        # 1. Move the two initial characters to the end of the string, replacing checksum for '00'
        value = value[4:] + value[:2] + '00'

        # 2. Replace each letter in the string with two digits, thereby expanding the string, where
        #    A = 10, B = 11, ..., Z = 35.
        value_digits = ''
        for x in value:
            if '0' <= x <= '9':
                value_digits += x
            elif 'A' <= x <= 'Z':
                value_digits += str(ord(x) - 55)
            else:
                raise ValidationError(_('%s is not a valid character for IBAN.') % x)

        # 3. The remainder of the number above when divided by 97 is then subtracted from 98.
        return '%02d' % (98 - int(value_digits) % 97)

    def __call__(self, value):
        """
        Validates the IBAN value using the official IBAN validation algorithm.
        https://en.wikipedia.org/wiki/International_Bank_Account_Number#Validating_the_IBAN
        """
        if value is None:
            return value

        value = value.upper().replace(' ', '').replace('-', '')

        # Check that the total IBAN length is correct as per the country. If not, the IBAN is invalid.
        country_code = value[:2]
        if country_code in self.validation_countries:

            if self.validation_countries[country_code] != len(value):
                msg_params = {'country_code': country_code, 'number': self.validation_countries[country_code]}
                raise ValidationError(_('%(country_code)s IBANs must contain %(number)s characters.') % msg_params)

        else:
            raise ValidationError(_('%s is not a valid country code for IBAN.') % country_code)
        if self.include_countries and country_code not in self.include_countries:
            raise ValidationError(_('%s IBANs are not allowed in this field.') % country_code)

        if self.iban_checksum(value) != value[2:4]:
            raise ValidationError(_('Not a valid IBAN.'))


@deconstructible
class BICValidator:
    """
    A validator for SWIFT Business Identifier Codes (ISO 9362:2009).
    Validation is based on the BIC structure found on wikipedia.
    https://en.wikipedia.org/wiki/ISO_9362#Structure
    """

    def __eq__(self, other):
        # There is no outside modification of properties so this should always be true by default.
        return True

    def __call__(self, value):
        if value is None:
            return value

        value = value.upper()

        # Length is 8 or 11.
        bic_length = len(value)
        if bic_length != 8 and bic_length != 11:
            raise ValidationError(_('BIC codes have either 8 or 11 characters.'))

        # BIC is alphanumeric
        if any(char not in string.ascii_uppercase + string.digits for char in value):
            raise ValidationError(_('BIC codes only contain alphabet letters and digits.'))

        # First 4 letters are A - Z.
        institution_code = value[:4]
        if any(char not in string.ascii_uppercase for char in institution_code):
            raise ValidationError(_('%s is not a valid institution code.') % institution_code)

        # Letters 5 and 6 consist of an ISO 3166-1 alpha-2 country code.
        country_code = value[4:6]
        if country_code not in ISO_3166_1_ALPHA2_COUNTRY_CODES:
            raise ValidationError(_('%s is not a valid country code.') % country_code)

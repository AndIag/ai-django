from django import forms

from ai_django.ai_core.validators.bank import IBANValidator, BICValidator, IBAN_COUNTRY_CODE_LENGTH

IBAN_MIN_LENGTH = min(IBAN_COUNTRY_CODE_LENGTH.values())


class IBANFormField(forms.CharField):
    """
    An IBAN consists of up to 34 alphanumeric characters.
    To limit validation to specific countries, set the 'include_countries' argument with a tuple or list of ISO 3166-1
    alpha-2 codes. For example, `include_countries=('NL', 'BE, 'LU')`.
    A list of countries that use IBANs as part of SEPA is included for convenience. To use this feature, set
    `include_countries=IBAN_SEPA_COUNTRIES` as an argument to the field.
    Example:
    .. code-block:: python
        from django import forms
        from localflavor.generic.forms import IBANFormField
        from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES
        class MyForm(forms.Form):
            iban = IBANFormField(include_countries=IBAN_SEPA_COUNTRIES)
    In addition to validating official IBANs, this field can optionally validate unofficial IBANs that have been
    catalogued by Nordea by setting the `use_nordea_extensions` argument to True.
    https://en.wikipedia.org/wiki/International_Bank_Account_Number
    .. versionadded:: 1.1
    """
    def __init__(self, use_nordea_extensions=False, include_countries=None, *args, **kwargs):
        kwargs.setdefault('min_length', IBAN_MIN_LENGTH)
        kwargs.setdefault('max_length', 34)
        self.default_validators = [IBANValidator(use_nordea_extensions, include_countries)]
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return self.empty_value
        return value.upper().replace(' ', '').replace('-', '')

    def prepare_value(self, value):
        """The display format for IBAN has a space every 4 characters."""
        if value is None:
            return value
        grouping = 4
        value = value.upper().replace(' ', '').replace('-', '')
        return ' '.join(value[i:i + grouping] for i in range(0, len(value), grouping))


class BICFormField(forms.CharField):
    """
    A BIC consists of 8 (BIC8) or 11 (BIC11) alphanumeric characters.
    BICs are also known as SWIFT-BIC, BIC code, SWIFT ID, SWIFT code or ISO 9362.
    https://en.wikipedia.org/wiki/ISO_9362
    .. versionadded:: 1.1
    """

    default_validators = [BICValidator()]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 11)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        # BIC is always written in upper case.
        # https://www2.swift.com/uhbonline/books/public/en_uk/bic_policy/bic_policy.pdf
        value = super().to_python(value)
        if value in self.empty_values:
            return self.empty_value
        return value.upper().replace(" ", "")

    def prepare_value(self, value):
        # BIC is always written in upper case.
        value = super().prepare_value(value)
        if value is not None:
            return value.upper()
        return value

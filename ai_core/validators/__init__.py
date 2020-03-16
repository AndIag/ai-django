from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from ai_django.ai_core.validators.bank import BICValidator, IBANValidator
from ai_django.ai_core.validators.base import DNIValidator
from ai_django.ai_core.validators.schema import JSONSchemaValidator

PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("PHONE_REGEX_ERROR"))

__all__ = [PHONE_REGEX, DNIValidator, BICValidator, IBANValidator, JSONSchemaValidator]

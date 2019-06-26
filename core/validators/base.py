from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("PHONE_REGEX_ERROR"))


@deconstructible
class DNIValidator(object):
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    external = "XYZ"
    external_map = {'X': '0', 'Y': '1', 'Z': '2'}
    numbers = "1234567890"

    def __call__(self, value):
        dni = value.upper()
        if len(dni) == 9:
            dig_control = dni[8]
            dni = dni[:8]
            if dni[0] in self.external:
                dni = dni.replace(dni[0], self.external_map[dni[0]])
            return len(dni) == len([n for n in dni if n in self.numbers]) and self.tabla[int(dni) % 23] == dig_control
        return False

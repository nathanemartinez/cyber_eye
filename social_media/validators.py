from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import json


def validate_dictionary_from_json(value):
    value = json.loads(value)
    if type(value) is not dict:
        raise ValidationError(
            _(f'{value} is not a valid dictionary'),
            params={'value': value},
        )


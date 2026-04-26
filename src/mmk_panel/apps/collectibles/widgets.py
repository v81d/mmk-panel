from django import forms


class MoveEffectPairWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.NumberInput(attrs={"placeholder": "Amplitude"}),
            forms.NumberInput(attrs={"placeholder": "Duration"}),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value is None:
            return [None, None]

        if isinstance(value, (list, tuple)) and len(value) == 2:
            return [value[0], value[1]]

        return [None, None]


class MoveEffectPairField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.FloatField(required=False),
            forms.FloatField(required=False),
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if not data_list:
            return None

        amp, duration = data_list

        if amp in (None, "") and duration in (None, ""):
            return None

        return [amp, duration]

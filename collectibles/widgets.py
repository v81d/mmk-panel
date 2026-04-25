from django import forms
from django.utils.safestring import mark_safe

UNFOLD_INPUT_CLASSES = "border border-base-200 bg-white font-medium min-w-20 placeholder-base-400 rounded-default shadow-xs text-font-default-light text-sm focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 group-[.errors]:border-red-600 focus:group-[.errors]:outline-red-600 dark:bg-base-900 dark:border-base-700 dark:text-font-default-dark dark:group-[.errors]:border-red-500 dark:focus:group-[.errors]:outline-red-500 dark:scheme-dark group-[.primary]:border-transparent disabled:!bg-base-50 dark:disabled:!bg-base-800 px-3 py-2 w-full max-w-2xl"


class MoveEffectPairWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.NumberInput(
                attrs={"placeholder": "Amplitude", "class": UNFOLD_INPUT_CLASSES}
            ),
            forms.NumberInput(
                attrs={"placeholder": "Duration", "class": UNFOLD_INPUT_CLASSES}
            ),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value is None:
            return [None, None]

        if isinstance(value, (list, tuple)) and len(value) == 2:
            return [value[0], value[1]]

        return [None, None]

    def render(self, name, value, attrs=None, renderer=None):
        rendered = super().render(name, value, attrs, renderer)
        return mark_safe(
            f'<div class="flex gap-2 max-w-2xl">{rendered}</div>'
        )  # gap between inputs


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

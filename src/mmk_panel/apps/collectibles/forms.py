from django import forms

from .models import Move
from .widgets import MoveEffectPairField, MoveEffectPairWidget


class MoveAdminForm(forms.ModelForm):
    self_defense_multipler = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    self_attack_multipler = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    self_move_energy_multipler = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    self_move_energy_gain_multipler = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    self_desperation_multipler = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    self_defense_scalar_boost = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    self_attack_scalar_boost = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    self_move_energy_scalar_boost = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    self_move_energy_gain_scalar_boost = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    self_poison = MoveEffectPairField(widget=MoveEffectPairWidget(), required=False)

    enemy_defense_multiplier = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    enemy_attack_multiplier = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    enemy_move_energy_multiplier = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    enemy_move_energy_gain_multiplier = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    enemy_desperation_multiplier = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    enemy_defense_scalar_boost = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    enemy_attack_scalar_boost = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    enemy_move_energy_scalar_boost = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    enemy_move_energy_gain_scalar_boost = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    enemy_desperation_scalar_boost = MoveEffectPairField(
        widget=MoveEffectPairWidget(), required=False
    )
    enemy_poison = MoveEffectPairField(widget=MoveEffectPairWidget(), required=False)

    class Meta:
        model = Move
        fields = "__all__"

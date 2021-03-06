# coding: utf-8

from dext.forms import forms, fields

from utg import relations as utg_relations

from the_tale.common.utils import bbcode

from the_tale.linguistics.forms import WordField

from the_tale.game import relations as game_relations

from the_tale.game.companions import relations

from the_tale.game.balance import constants as c

from the_tale.game.companions.abilities import forms as abilities_forms


class CompanionRecordForm(forms.Form):

    name = WordField(word_type=utg_relations.WORD_TYPE.NOUN, label=u'Название')

    max_health = fields.IntegerField(label=u'здоровье', min_value=c.COMPANIONS_MIN_HEALTH, max_value=c.COMPANIONS_MAX_HEALTH)

    type = fields.RelationField(label=u'тип', relation=relations.TYPE)
    dedication = fields.RelationField(label=u'самоотверженность', relation=relations.DEDICATION)
    archetype = fields.RelationField(label=u'архетип', relation=game_relations.ARCHETYPE)
    mode = fields.RelationField(label=u'режим появления в игре', relation=relations.MODE)

    abilities = abilities_forms.AbilitiesField(label=u'', required=False)

    description = bbcode.BBField(label=u'Описание', required=False)

    @classmethod
    def get_initials(cls, companion):
        return {'description': companion.description,
                'max_health': companion.max_health,
                'type': companion.type,
                'dedication': companion.dedication,
                'archetype': companion.archetype,
                'mode': companion.mode,
                'abilities': companion.abilities,
                'name': companion.utg_name}

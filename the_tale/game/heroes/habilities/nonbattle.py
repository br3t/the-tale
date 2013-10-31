# coding: utf-8
import random

from game.game_info import ATTRIBUTES
from game.heroes.habilities.prototypes import AbilityPrototype
from game.heroes.habilities.relations import ABILITY_TYPE, ABILITY_ACTIVATION_TYPE, ABILITY_AVAILABILITY
from game.heroes.relations import ITEMS_OF_EXPENDITURE


class CHARISMA(AbilityPrototype):

    TYPE = ABILITY_TYPE.NONBATTLE
    ACTIVATION_TYPE = ABILITY_ACTIVATION_TYPE.PASSIVE
    AVAILABILITY = ABILITY_AVAILABILITY.FOR_PLAYERS

    NAME = u'Харизматичный'
    normalized_name = NAME
    DESCRIPTION = u'Герой настолько обаятелен, что умудряется получать больше денег за выполнение заданий.'

    MONEY_MULTIPLIER = [2, 2.5, 3, 3.5, 4]

    @property
    def money_multiplier(self): return self.MONEY_MULTIPLIER[self.level-1]

    def update_quest_reward(self, hero, money):
        return int(money * self.money_multiplier)


class HUCKSTER(AbilityPrototype):

    TYPE = ABILITY_TYPE.NONBATTLE
    ACTIVATION_TYPE = ABILITY_ACTIVATION_TYPE.PASSIVE
    AVAILABILITY = ABILITY_AVAILABILITY.FOR_PLAYERS

    NAME = u'Торгаш'
    normalized_name = NAME
    DESCRIPTION = u'Увеличивается цена продажи и уменьшается цена покупки предметов.'

    SELL_MULTIPLIER = [1.1, 1.15, 1.2, 1.25, 1.3]
    BUY_MULTIPLIER = [0.9, 0.85, 0.8, 0.75, 0.7]

    @property
    def sell_multiplier(self): return self.SELL_MULTIPLIER[self.level-1]

    @property
    def buy_multiplier(self): return self.BUY_MULTIPLIER[self.level-1]

    def update_buy_price(self, hero, money):
        return int(money * self.buy_multiplier)

    def update_sell_price(self, hero, money):
        ''' +1 for increase price on low levels'''
        return int(money * self.sell_multiplier + 1)


class DANDY(AbilityPrototype):

    TYPE = ABILITY_TYPE.NONBATTLE
    ACTIVATION_TYPE = ABILITY_ACTIVATION_TYPE.PASSIVE
    AVAILABILITY = ABILITY_AVAILABILITY.FOR_PLAYERS

    NAME = u'Щёголь'
    normalized_name = NAME
    DESCRIPTION = u'Увеличивает вероятность траты денег на заточку и покупку артефактов.'

    PRIORITY_MULTIPLIER = [1.5, 2, 2.5, 3, 3.5]

    @property
    def priority_multiplier(self): return self.PRIORITY_MULTIPLIER[self.level-1]

    def update_items_of_expenditure_priorities(self, hero, priorities):
        priorities[ITEMS_OF_EXPENDITURE.BUYING_ARTIFACT] *= self.priority_multiplier
        priorities[ITEMS_OF_EXPENDITURE.SHARPENING_ARTIFACT] *= self.priority_multiplier
        return priorities


class BUSINESSMAN(AbilityPrototype):

    TYPE = ABILITY_TYPE.NONBATTLE
    ACTIVATION_TYPE = ABILITY_ACTIVATION_TYPE.PASSIVE
    AVAILABILITY = ABILITY_AVAILABILITY.FOR_PLAYERS

    NAME = u'Делец'
    normalized_name = NAME
    DESCRIPTION = u'Герой может получить артефакт в награду за выполнение задания.'

    PROBABILITY = [0.05, 0.1, 0.15, 0.2, 0.25]

    @property
    def probability(self): return self.PROBABILITY[self.level-1]

    def can_get_artifact_for_quest(self, hero):
        return random.uniform(0, 1) < self.probability


class PICKY(AbilityPrototype):

    TYPE = ABILITY_TYPE.NONBATTLE
    ACTIVATION_TYPE = ABILITY_ACTIVATION_TYPE.PASSIVE
    AVAILABILITY = ABILITY_AVAILABILITY.FOR_PLAYERS

    NAME = u'Придирчивый'
    normalized_name = NAME
    DESCRIPTION = u'Герой с большей вероятностью покупает полезные артефакты (лучше, чем экипированные).'

    PROBABILITY = [0.05, 0.1, 0.15, 0.2, 0.25]

    @property
    def probability(self): return self.PROBABILITY[self.level-1]

    def can_buy_better_artifact(self, hero):
        return random.uniform(0, 1) < self.probability

class ETHEREAL_MAGNET(AbilityPrototype):

    TYPE = ABILITY_TYPE.NONBATTLE
    ACTIVATION_TYPE = ABILITY_ACTIVATION_TYPE.PASSIVE
    AVAILABILITY = ABILITY_AVAILABILITY.FOR_PLAYERS

    NAME = u'Эфирный магнит'
    normalized_name = NAME
    DESCRIPTION = u'Герой притягивает к себе магию и увеличивает вероятность критического срабатывания помощи хранителя.'

    CRIT_PROBABILITY = [0.04, 0.08, 0.12, 0.16, 0.20]

    @property
    def crit_probability(self): return self.CRIT_PROBABILITY[self.level-1]

    def modify_attribute(self, type_, value): return min(1.0, value + self.crit_probability) if type_ == ATTRIBUTES.MIGHT_CRIT_CHANCE else value


class WANDERER(AbilityPrototype):

    TYPE = ABILITY_TYPE.NONBATTLE
    ACTIVATION_TYPE = ABILITY_ACTIVATION_TYPE.PASSIVE
    AVAILABILITY = ABILITY_AVAILABILITY.FOR_PLAYERS

    NAME = u'Бродяга'
    normalized_name = NAME
    DESCRIPTION = u'Бродяги истоптали тысячи тропинок и всегда найдут кратчайшую дорогу, поэтому путешествуют быстрее остальных.'

    # since experience not depends on time, this agruments MUST be equal or less then GIFTER.EXPERIENCE_MULTIPLIER
    # in other case, GIFTED will give less experience, then WANDERER
    SPEED_MULTIPLIER = [1.04, 1.08, 1.12, 1.16, 1.20]

    @property
    def speed_multiplier(self): return self.SPEED_MULTIPLIER[self.level-1]

    def modify_attribute(self, type_, value): return value*self.speed_multiplier if type_ == ATTRIBUTES.SPEED else value


class GIFTED(AbilityPrototype):

    TYPE = ABILITY_TYPE.NONBATTLE
    ACTIVATION_TYPE = ABILITY_ACTIVATION_TYPE.PASSIVE
    AVAILABILITY = ABILITY_AVAILABILITY.FOR_PLAYERS

    NAME = u'Одарённый'
    normalized_name = NAME
    DESCRIPTION = u'Одарённые герои быстрее получают опыт.'

    EXPERIENCE_MULTIPLIER = [1.05, 1.1, 1.15, 1.2, 1.25]

    @property
    def experience_multiplier(self): return self.EXPERIENCE_MULTIPLIER[self.level-1]

    def modify_attribute(self, type_, value): return value*self.experience_multiplier if type_ == ATTRIBUTES.EXPERIENCE else value


ABILITIES = dict( (ability.get_id(), ability)
                  for ability in globals().values()
                  if isinstance(ability, type) and issubclass(ability, AbilityPrototype) and ability != AbilityPrototype)

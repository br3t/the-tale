# coding: utf-8
import math

from the_tale.game.balance import enums as e
from the_tale.game.balance import helpers as h

TIME_TO_LVL_DELTA = float(5) # разница во времени получения двух соседних уровней

INITIAL_HP = int(500) # начальное здоровье героя

HP_PER_LVL = int(50) # бонус к здоровью на уровень

MOB_HP_MULTIPLIER = float(0.25) # какой процент здоровье среднего моба составляет от здоровья героя
BOSS_HP_MULTIPLIER = float(0.5) # какой процент здоровье среднего моба составляет от здоровья героя

TURN_DELTA = int(10)  # в секундах - задержка одного хода

TURNS_IN_HOUR = float(60.0 * 60 / TURN_DELTA) # количество ходов в 1 часе

POWER_PER_LVL = int(1) # значение "чистой" силы героя (т.е. без артефактов)

EQUIP_SLOTS_NUMBER = int(11) # количество слотов экипировки

ARTIFACTS_PER_LVL = int(4) # количество новых артефактов, на уровень героя

EXP_PENALTY_MULTIPLIER = float(0.1) # процент опыта при замедленной прокачке
EXP_PER_HOUR = int(10)  # опыт в час
EXP_PER_QUEST_FRACTION = float(0.33) # разброс опыта за задание

EXP_FOR_PREMIUM_ACCOUNT = float(1.0) # модификатор опыта для премиум аккаунтов
EXP_FOR_NORMAL_ACCOUNT = float(0.66) # модификатор опыта для обычных акканутов

# TODO: привести EXP_FOR_PREMIUM_ACCOUNT к 1.0 (разница с нормальным аккаунтом должна быть 50%)
#       сейчас это сделать нельзя т.к. паливо


HERO_MOVE_SPEED = float(0.3) # базовая скорость героя расстояние в ход

BATTLE_LENGTH = int(16) # ходов - средняя длительность одного боя (количество действий в бой)
INTERVAL_BETWEEN_BATTLES = int(3) # ходов - время, между двумя битвами

BATTLES_BEFORE_HEAL = int(8) # количество боёв в непрерывной цепочке битв

HEAL_TIME_FRACTION = float(0.2) # доля времени от цепочки битв, которую занимает полный отхил героя
HEAL_STEP_FRACTION = float(0.2) # разброс регенерации за один ход

HEALTH_IN_SETTLEMENT_TO_START_HEAL_FRACTION = float(0.33) # если у героя здоровья меньше, чем указанная доля и он в городе, то он будет лечиться
HEALTH_IN_MOVE_TO_START_HEAL_FRACTION = float(2 * (1.0 / BATTLES_BEFORE_HEAL)) # если у героя здоровья меньше, чем указанная доля и он в походе, то он будет лечиться

TURNS_TO_IDLE = int(6) # количество ходов на уровень, которое герой бездельничает в соответствующей action
TURNS_TO_RESURRECT = int(TURNS_TO_IDLE * 3) # количество ходов на уровень, необходимое для воскрешения


GET_LOOT_PROBABILITY = float(0.33) # вероятность получить добычу после боя, если не получен артефакт

# вероятности получить разный тип добычи

NORMAL_LOOT_PROBABILITY = float(0.99)
RARE_LOOT_PROBABILITY = float(0.0099)
EPIC_LOOT_PROBABILITY = 1 - NORMAL_LOOT_PROBABILITY - RARE_LOOT_PROBABILITY

#стоимость разной добычи на единицу уровня
NORMAL_LOOT_COST = float(1.5)
RARE_LOOT_COST = float(25)
EPIC_LOOT_COST = float(250)

MAX_BAG_SIZE = int(12) # максимальный размер рюкзака героя
BAG_SIZE_TO_SELL_LOOT_FRACTION = float(0.33) # процент заполненности рюкзака, после которого герой начнёт продавать вещи

# относительные размеры различных трат

# эвристический мультипликатор для нормальной цены дейсвия, учитывающий стронние доходы
# не учтённые в формулах (доходы по заданиям и прочему)
NORMAL_ACTION_PRICE_MULTIPLYER = float(1.2)

BASE_EXPERIENCE_FOR_MONEY_SPEND = int(24 * EXP_PER_HOUR * 0.4)
EXPERIENCE_DELTA_FOR_MONEY_SPEND = float(0.5)

SELL_ARTIFACT_PRICE_FRACTION = float(0.15) # часть дневного дохода, за которую артефакты продаются

PRICE_DELTA = float(0.2) # дельта на цену PRICE * (1 + random.uniform(-0.2, 0.2))

POWER_TO_LVL = float(EQUIP_SLOTS_NUMBER) # бонус к ожидаемой силе на уровнеь героя

# Разброс силы артефактов делаем от -ItemPowerDelta до +ItemPowerDelta.
# за базу берём количество слотов, т.е., теоретически, может не быть предметов с повторяющейся силой
# что бы не вводить дизбаланса, надо на маленьких уровнях уменьшать делту, что бу разница уровня предмета и дельты была неменьше единицы
ARTIFACT_POWER_DELTA = float(0.2) # дельта, на которую может изменяться сила артифакта

# ходов - длинна непрерывной цепочки боёв до остановки на лечение
BATTLES_LINE_LENGTH = int(BATTLES_BEFORE_HEAL * (BATTLE_LENGTH + INTERVAL_BETWEEN_BATTLES ) - INTERVAL_BETWEEN_BATTLES)

# количество битв в ход в промежутке непрерывных боёв
BATTLES_PER_TURN = float(1.0 / (INTERVAL_BETWEEN_BATTLES + 1) )

HEAL_LENGTH = int(math.floor(BATTLES_LINE_LENGTH * HEAL_TIME_FRACTION)) # ходов - длительность лечения героя

ACTIONS_CYCLE_LENGTH = int(BATTLES_LINE_LENGTH + HEAL_LENGTH) # ходов - длинна одного "игрового цикла" - цепочка боёв + хил

# примерное количество боёв, которое будет происходить в час игрового времени
BATTLES_PER_HOUR = TURNS_IN_HOUR * (float(BATTLES_BEFORE_HEAL) / ACTIONS_CYCLE_LENGTH)


DAMAGE_TO_HERO_PER_HIT_FRACTION = float(1.0 / (BATTLES_BEFORE_HEAL * BATTLE_LENGTH / 2)) # доля урона, наносимого герою за удар
DAMAGE_TO_MOB_PER_HIT_FRACTION = float(1.0 / (BATTLE_LENGTH / 2)) # доля урона, наносимого мобу за удар
DAMAGE_DELTA = float(0.2) # разброс в значениях урона [1-DAMAGE_DELTA, 1+DAMAGE_DELTA]

DAMAGE_CRIT_MULTIPLIER = float(2.0) # во сколько раз увеличивается урон при критическом ударе

# таким образом, напрашиваются следующие параметры мобов:
# - здоровье, в долях от среднемобского - чем больше его, тем  дольше моб живёт
#  - инициатива, в долях относительно геройской - чем больше, тем чаще моб ходит
#  - урон, в долях от среднемобского - чем больше, тем больнее бьёт
#  - разброс урона, в долях от среднего - декоративный параметр, т.к. в итоге будет средний урон наноситься
# так как все параметры измеряются в долях, то сложность моба можно высчитать как hp * initiative * damage = 1 для среднего моба
# моб со всеми парамтрами, увеличеными на 10% будет иметь сложность 1.1^3 ~ 1.33
# соответственно, вводня для каждого параметра шаг в 0.1 и скалируя от 0.5 до 1.5, получим 11^3 вариантов параметров (и, соответственно поведения)
# сложность мобов в этом случае будет изменяться от 0.5^3 до 1.5^3 ~ (0.125, 3.375)
#
# возникает проблема обеспечения равномерности прокачки героев на разных территориях - для полностью честных условий необходимо обеспечить одинаковую сложность мобов,
# альтернативный вариант - изменять количесво опыта, даваемого за моба, в зависимости от его сложности, этот вариант кажется как более логичным с точки зрения игрока, так и простым в реализации, на нём и остановимся
#
# расчёт прочей добычи и золота: добыча/трата

# считаем, что если герой не выбил артефакт, то у него есть вероятность выбить добычу
# добычу делим на обычную, редкую и очень редкую
# добыча является основным источником дохода, вырученное за его продажу золото является функцией от уровня и редкости - т.е. есть три фунции от уровня
# добыча, как и мобы, организован в список, отсортированый по уровню, на котором он становится доступным, это позволит открывать игрокам новый контент, а так же сделать разброс цен



##########################
# разные левые "неприкаянные" константы
##########################

DESTINY_POINT_IN_LEVELS = int(5) # раз в сколько уровней давать очко абилок
SPEND_MONEY_FOR_HEAL_HEALTH_FRACTION = float(0.75) # герой будет тратить деньги на лечение, когда его здоровье будет меньше этого параметра

##########################
# параметры ангелов
##########################

# енергия должна полностью регенериться за сутки, раз в 2 часа должна появляться новая мажка
ANGEL_ENERGY_MAX = int(12) # всего энергии
ANGEL_ENERGY_PREMIUM_BONUS = int(ANGEL_ENERGY_MAX * 0.5) # бонус к максимуму энергии для премов
ANGEL_FREE_ENERGY_MAXIMUM = int(50) # максимальное количество энергии, которые игрок может получить, используя помощь
ANGEL_FREE_ENERGY_CHARGE = int(10) # количество бонусной энергии при срабатывании помощи
ANGEL_FREE_ENERGY_CHARGE_CRIT = int(20)# количество бонусной энергии при критическом срабатывании помощи


# TODO: возможно, надо перебалансить всё зависимое от ANGEL_ENERGY_MAX с учётом ANGEL_ENERGY_PREMIUM_BONUS

ANGEL_ENERGY_REGENERATION_TIME = float(0.5) # раз в сколько часов регенерируем
ANGEL_ENERGY_REGENERATION_AMAUNT = int(1) # сколько восстанавливаем
ANGEL_ENERGY_REGENERATION_PERIOD = int(ANGEL_ENERGY_REGENERATION_TIME * TURNS_IN_HOUR) # раз в сколько ходов
_ANGEL_ENERGY_IN_DAY = int(24.0 / ANGEL_ENERGY_REGENERATION_TIME * ANGEL_ENERGY_REGENERATION_AMAUNT)


ANGEL_ENERGY_REGENERATION_DELAY = { e.ANGEL_ENERGY_REGENERATION_TYPES.PRAY: 1,
                                    e.ANGEL_ENERGY_REGENERATION_TYPES.SACRIFICE: 2,
                                    e.ANGEL_ENERGY_REGENERATION_TYPES.INCENSE: 4,
                                    e.ANGEL_ENERGY_REGENERATION_TYPES.SYMBOLS: 3,
                                    e.ANGEL_ENERGY_REGENERATION_TYPES.MEDITATION: 2 }

ANGEL_ENERGY_REGENERATION_STEPS = { e.ANGEL_ENERGY_REGENERATION_TYPES.PRAY: 3,
                                    e.ANGEL_ENERGY_REGENERATION_TYPES.SACRIFICE: 5,
                                    e.ANGEL_ENERGY_REGENERATION_TYPES.INCENSE: 6,
                                    e.ANGEL_ENERGY_REGENERATION_TYPES.SYMBOLS: 4,
                                    e.ANGEL_ENERGY_REGENERATION_TYPES.MEDITATION: 4 }

##########################
# абилки ангела
##########################

ANGEL_HELP_COST = 4

ANGEL_HELP_HEAL_IF_LOWER_THEN = float(0.8) # можем лечить если здоровья меньше чем

ANGEL_HELP_HEAL_FRACTION = (float(0.25), float(0.5)) # (min, max) процент хелсов, которые будут вылечины
ANGEL_HELP_TELEPORT_DISTANCE = float(3.0) # расстяние на которое происходит телепорт
ANGEL_HELP_LIGHTING_FRACTION = (float(0.25), float(0.5)) # (min, max) процент урона, который будет нанесён

# считаем, что при эпической удачливости все использования будут давать опыт
# и предполагаем, что можем разрешить (при такой удачливости), в день получать опыт как за такой же день
ANGEL_HELP_EXPERIENCE = int(24.0 * EXP_PER_HOUR / (_ANGEL_ENERGY_IN_DAY / ANGEL_HELP_COST))

ANGEL_HELP_EXPERIENCE_DELTA = float(0.5)

ANGEL_HELP_CRIT_HEAL_FRACTION = (float(0.5), float(0.75)) # (min, max) процент хелсов, которые будут вылечины
ANGEL_HELP_CRIT_TELEPORT_DISTANCE = float(9.0) # расстяние на которое происходит телепорт
ANGEL_HELP_CRIT_LIGHTING_FRACTION = (float(0.5), float(0.75)) # (min, max) процент урона, который будет нанесён
ANGEL_HELP_CRIT_MONEY_MULTIPLIER = int(10)
ANGEL_HELP_CRIT_EXPERIENCE = int(ANGEL_HELP_EXPERIENCE * 3)


ANGEL_ENERGY_INSTANT_REGENERATION_IN_PLACE = ANGEL_HELP_COST

##########################
# игровое время из расчёта 1/4 дня в полчаса (считаем среднюю сессию в 15 минут, берём х2 запас), т.е. 1 игровой день == 2 часа реального времени
##########################

GAME_SECONDS_IN_GAME_MINUTE = int(60)
GAME_MINUTES_IN_GAME_HOUR = int(60)
GAME_HOURSE_IN_GAME_DAY = int(24)
GAME_DAYS_IN_GAME_WEEK = int(7)
GAME_WEEKS_IN_GAME_MONTH = int(4)
GAME_MONTH_IN_GAME_YEAR = int(4)

GAME_SECONDS_IN_GAME_HOUR = int(GAME_SECONDS_IN_GAME_MINUTE * GAME_MINUTES_IN_GAME_HOUR)
GAME_SECONDS_IN_GAME_DAY = int(GAME_SECONDS_IN_GAME_HOUR * GAME_HOURSE_IN_GAME_DAY)
GAME_SECONDS_IN_GAME_WEEK = int(GAME_SECONDS_IN_GAME_DAY * GAME_DAYS_IN_GAME_WEEK)
GAME_SECONDS_IN_GAME_MONTH = int(GAME_SECONDS_IN_GAME_WEEK * GAME_WEEKS_IN_GAME_MONTH)
GAME_SECONDS_IN_GAME_YEAR = int(GAME_SECONDS_IN_GAME_MONTH * GAME_MONTH_IN_GAME_YEAR)

_TURNS_IN_GAME_DAY = int(4 *(TURNS_IN_HOUR / 2))

TURNS_IN_GAME_MONTH = _TURNS_IN_GAME_DAY * GAME_DAYS_IN_GAME_WEEK * GAME_WEEKS_IN_GAME_MONTH
TURNS_IN_GAME_YEAR = TURNS_IN_GAME_MONTH * GAME_MONTH_IN_GAME_YEAR
GAME_SECONDS_IN_TURN = int(GAME_SECONDS_IN_GAME_DAY / _TURNS_IN_GAME_DAY)

##########################
# Карта
##########################

MAP_CELL_LENGTH = float(3.0) # длина клетки в километрах

MAP_SYNC_TIME_HOURS = int(1)
MAP_SYNC_TIME = int(TURNS_IN_HOUR * MAP_SYNC_TIME_HOURS) # синхронизируем карту раз в N часов

##########################
# Задания
##########################

QUESTS_SHORT_PATH_LEVEL_CAP = int(4) # на уровнях до этого герои получаю задания в близких городах

QUESTS_PILGRIMAGE_FRACTION = float(0.025) # вероятность отправить героя в паломничество

##########################
# Влияние
##########################

HERO_POWER_PER_DAY = int(1000) # базовое количество влияния, которое герой 1-ого уровня производит в день на одного жителя задействованного в заданиях
PERSON_POWER_PER_QUEST_FRACTION = float(0.33) # разброс влияния за задание
PERSON_POWER_FOR_RANDOM_SPEND = int(200) # доля от стандартной величины..
HERO_POWER_PREFERENCE_MULTIPLIER = int(2) # множитель для начисления влияния связанного с предпочтениями

CHARACTER_PREFERENCES_CHANGE_DELAY = int(60*60*24*7) # время блокировки возможности изменять предпочтение

##########################
# споособности
##########################

ABILITIES_ACTIVE_MAXIMUM = int(5)
ABILITIES_PASSIVE_MAXIMUM = int(2)

ABILITIES_BATTLE_MAXIMUM = ABILITIES_ACTIVE_MAXIMUM + ABILITIES_PASSIVE_MAXIMUM
ABILITIES_NONBATTLE_MAXUMUM = int(4)

ABILITIES_OLD_ABILITIES_FOR_CHOOSE_MAXIMUM = int(2)
ABILITIES_FOR_CHOOSE_MAXIMUM = int(4)

##########################
# Черты
##########################

HABITS_BORDER = int(1000) # модуль максимального значения черты
HABITS_RIGHT_BORDERS = [-700, -300, -100, 100, 300, 700, 1001] # правые границы черт
HABITS_QUEST_ACTIVE_DELTA = float(5) # за выбор в заданиии гроком
HABITS_QUEST_PASSIVE_DELTA = float(0.1 * HABITS_QUEST_ACTIVE_DELTA) # за неверный выбор героем
HABITS_ABILITY_DELTA = float(HABITS_BORDER / (30 * _ANGEL_ENERGY_IN_DAY / ANGEL_HELP_COST)) # за использование способности
HABITS_PERIODIC_DELTA = float(0.1 * (HABITS_QUEST_ACTIVE_DELTA*2 + HABITS_ABILITY_DELTA * (_ANGEL_ENERGY_IN_DAY / ANGEL_HELP_COST))/2 ) # скорость автоматического уменьшения (в день)

KILL_BEFORE_BATTLE_PROBABILITY = float(0.05)  # вероятность убить мобы в начале боя
PICKED_UP_IN_ROAD_TELEPORT_LENGTH = ANGEL_HELP_TELEPORT_DISTANCE
# бонус к скорости передвижения, эквивалентный вероятности убить моба
PICKED_UP_IN_ROAD_SPEED_BONUS = h.speed_from_safety(BATTLES_PER_TURN*KILL_BEFORE_BATTLE_PROBABILITY, BATTLES_PER_TURN)
PICKED_UP_IN_ROAD_PROBABILITY = PICKED_UP_IN_ROAD_SPEED_BONUS / PICKED_UP_IN_ROAD_TELEPORT_LENGTH

HABIT_QUEST_PRIORITY_MODIFIER = float(2) # модификатор приоритета выбора заданий от предпочтений

HONOR_POWER_BONUS_FRACTION = float(0.25) # бонус к влиянию на для чести
MONSTER_TYPE_BATTLE_CRIT_MAX_CHANCE = float(0.02) # вероятность крита по типу монстра, если все монстры этого типа

HABIT_QUEST_REWARD_MAX_BONUS = float(0.25) # максимальный бонус к награде за задание при выборе, совпадающем с чертой
HABIT_GET_LOOT_PROBABILITY = float(0.07) # бонус к вероятности получить лут

PEACEFULL_BATTLE_PROBABILITY = float(0.01) # вероятность мирно разойтись с монстром, если все можно расходиться со всеми типами монстров

# вероятность получить опыт расчитывается исходя из:
# - средней величины получаемого опыта
# - ускорения прокачки от первого удара (вычитается)
# - проигрыша агрессивного использования способностей (молния) перед мирными (телепортом) (плюсуется)
# - лечение не учитываем, т.к. оно может быть применено и в бою и не в бою

# процент сохранённых ходов от первого удара
_FIRST_STRIKE_TURNS_BONUS = (0.5 * BATTLES_BEFORE_HEAL) / ACTIONS_CYCLE_LENGTH # выигрываем полхода в каждой битве

_HELPS_IN_TURN = (float(_ANGEL_ENERGY_IN_DAY) / ANGEL_HELP_COST) / TURNS_IN_HOUR / 24

# процент сохранённых ходов сражении, если только бьём молнией
_BATTLE_TURNS_BONUS = (float(BATTLE_LENGTH) * (sum(ANGEL_HELP_LIGHTING_FRACTION)/2) + HEAL_LENGTH * (sum(ANGEL_HELP_LIGHTING_FRACTION)/2) / BATTLES_BEFORE_HEAL) * _HELPS_IN_TURN

# процент сохранённых ходов движения, если только телепортируем
_TELEPORT_MOVE_TURNS = float(ANGEL_HELP_TELEPORT_DISTANCE) / HERO_MOVE_SPEED
_TELEPORT_SAVED_BATTLES = _TELEPORT_MOVE_TURNS/INTERVAL_BETWEEN_BATTLES
_TELEPORT_SAVED_TURNS =_TELEPORT_MOVE_TURNS + _TELEPORT_SAVED_BATTLES * BATTLE_LENGTH + HEAL_LENGTH * _TELEPORT_SAVED_BATTLES / BATTLES_BEFORE_HEAL
_TELEPORT_TURNS_BONUS = _TELEPORT_SAVED_TURNS * _HELPS_IN_TURN

# процент сохранённых ходов от мирного расхождения с монстрами
_PEACEFULL_TURNS_BONUS = PEACEFULL_BATTLE_PROBABILITY * float(BATTLES_BEFORE_HEAL * BATTLE_LENGTH) / ACTIONS_CYCLE_LENGTH

# print 'battles in day', TURNS_IN_HOUR * 24 / ACTIONS_CYCLE_LENGTH * BATTLES_BEFORE_HEAL
# print 'inverted', 1.0 / (TURNS_IN_HOUR * 24 / ACTIONS_CYCLE_LENGTH * BATTLES_BEFORE_HEAL)
# print 'strike', _FIRST_STRIKE_TURNS_BONUS
# print 'battle', _BATTLE_TURNS_BONUS
# print 'teleport', _TELEPORT_TURNS_BONUS

EXP_FOR_KILL = int(12*EXP_PER_HOUR) # средний опыт за убийство монстра
EXP_FOR_KILL_DELTA = float(0.5) # разброс опыта за убийство
EXP_FOR_KILL_PROBABILITY = float(0.01)


_KILLS_IN_HOUR = float(TURNS_IN_HOUR) / ACTIONS_CYCLE_LENGTH * BATTLES_BEFORE_HEAL
_REQUIRED_BONUS_EXP = _TELEPORT_TURNS_BONUS + _PEACEFULL_TURNS_BONUS - _BATTLE_TURNS_BONUS - _FIRST_STRIKE_TURNS_BONUS

# вероятность получить опыт за убийство моба
EXP_FOR_KILL_PROBABILITY = float(EXP_PER_HOUR * _REQUIRED_BONUS_EXP) / EXP_FOR_KILL / _KILLS_IN_HOUR

###########################
# pvp
###########################

DAMAGE_PVP_ADVANTAGE_MODIFIER = float(0.5) # на какую долю изменяется урон при максимальной разнице в преимуществе между бойцами
DAMAGE_PVP_FULL_ADVANTAGE_STRIKE_MODIFIER = float(5) # во сколько раз увеличится урон удара при максимальном преимушестве

PVP_MAX_ADVANTAGE_STEP = float(0.25)

PVP_ADVANTAGE_BARIER = float(0.95)
PVP_EFFECTIVENESS_EXTINCTION_FRACTION = float(0.1)

PVP_EFFECTIVENESS_STEP = float(10)
PVP_EFFECTIVENESS_INITIAL = float(300)

###########################
# типы городов
###########################

PLACE_TYPE_NECESSARY_BORDER = int(75)
PLACE_TYPE_ENOUGH_BORDER = int(50)

PLACE_GOODS_BONUS = int(100) # в час, соответственно PLACE_GOODS_BONUS * LEVEL — прирост/убыль товаров в городе
PLACE_GOODS_TO_LEVEL = int(PLACE_GOODS_BONUS * (1 + 3.0/2) * 24) # 1 город + 3 средних жителя за 24 часа
PLACE_GOODS_AFTER_LEVEL_UP = float(0.25) # процент товаров, остающихся при увеличении размера города
PLACE_GOODS_AFTER_LEVEL_DOWN = float(0.75) # процент товаров, возвращающихся при уменьшении размера города

# исходим из того, что в первую очередь надо балансировать вероятность нападения монстров как самый важный параметр
PLACE_SAFETY_FROM_BEST_PERSON = float(0.05)
PLACE_TRANSPORT_FROM_BEST_PERSON = h.speed_from_safety(PLACE_SAFETY_FROM_BEST_PERSON, BATTLES_PER_TURN)

# хотя на опыт свобода и не влияет, но на город оказывает такое-же влияние как и транспорт
PLACE_FREEDOM_FROM_BEST_PERSON = PLACE_TRANSPORT_FROM_BEST_PERSON

PLACE_MAX_EXCHANGED_NUMBER = int(3)

PLACE_RACE_CHANGE_DELTA_IN_DAY = float(0.1)
PLACE_RACE_CHANGE_DELTA = (PLACE_RACE_CHANGE_DELTA_IN_DAY * MAP_SYNC_TIME) / (24 * TURNS_IN_HOUR)

PLACE_ADD_PERSON_DELAY = int(24 * TURNS_IN_HOUR) # раз в сколько ходов можно добавлять советника

###########################
# здания
###########################

BUILDING_MASTERY_BONUS = float(0.15)

# на починку зданий игроки тратят энергию
# желательно, чтобы для единственного здания в городе эффект единичной траты энергии был заметен

BUILDING_FULL_DESTRUCTION_TIME = int(2*7*24) # in hours
BUILDING_AMORTIZATION_SPEED = float(1.0 / BUILDING_FULL_DESTRUCTION_TIME) # percents/hour

# единственное здание города  может поддерживаться одним человеком при условии траты всей энергии
BUILDING_FULL_REPAIR_ENERGY_COST = int(BUILDING_FULL_DESTRUCTION_TIME * ANGEL_ENERGY_REGENERATION_AMAUNT * ANGEL_ENERGY_REGENERATION_PERIOD / TURNS_IN_HOUR)

BUILDING_AMORTIZATION_MODIFIER = float(1.5) # цена ремонта здания зависит от количества зданий в городе и равно <цена>*BULDING_AMORTIZATION_MODIFIER^<количество зданий - 1>
BUILDING_WORKERS_ENERGY_COST = int(3) # цена вызова одного рабочего

BUILDING_PERSON_POWER_MULTIPLIER = float(1.1)
BUILDING_TERRAIN_POWER_MULTIPLIER = float(0.5) # building terrain power is percent from city power

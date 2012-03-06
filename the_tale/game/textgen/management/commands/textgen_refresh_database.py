# coding: utf-8
import os
import pymorphy

from django.core.management.base import BaseCommand

from dext.utils import s11n

from ...templates import Vocabulary, Dictionary, Template
from ...words import WordBase
from ...conf import textgen_settings

morph = pymorphy.get_morph(textgen_settings.PYMORPHY_DICTS_DIRECTORY)

class Command(BaseCommand):

    help = 'load texts into databse'

    def handle(self, *args, **options):

        vocabulary = Vocabulary()
        vocabulary.clear()

        dictionary = Dictionary()
        dictionary.clear()

        tech_vocabulary_file_name = os.path.join(textgen_settings.TEXTS_DIRECTORY, 'vocabulary.json')
        if not os.path.exists(tech_vocabulary_file_name):
            tech_vocabulary = {}
        else:
            with open(tech_vocabulary_file_name) as f:
                tech_vocabulary = s11n.from_json(f.read())

        for filename in os.listdir(textgen_settings.TEXTS_DIRECTORY):

            if not filename.endswith('.json'):
                continue
            
            if filename == 'vocabulary.json':
                continue

            texts_path = os.path.join(textgen_settings.TEXTS_DIRECTORY, filename)

            if not os.path.isfile(texts_path):
                continue

            group = filename[:-5]

            print 'load %s' % group

            with open(texts_path) as f:
                data = s11n.from_json(f.read())

                if group != data['prefix']:
                    raise Exception('filename MUST be equal to prefix')

                for suffix in data['types']:
                    if suffix == '':
                        raise Exception('type MUST be not equal to empty string')

                for suffix, type_ in data['types'].items():
                    phrase_key = '%s_%s' % (group , suffix)
                    for phrase in type_['phrases']:
                        template = Template.create(morph, phrase, available_externals=type_['variables'], tech_vocabulary=tech_vocabulary)
                        
                        vocabulary.add_phrase(phrase_key, template)
                        # print phrase

                        for string in template.get_internal_words():
                            word = WordBase.create_from_string(morph, string, tech_vocabulary)
                            dictionary.add_word(word)


        vocabulary.save()
        dictionary.save()

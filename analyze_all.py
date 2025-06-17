import re


class NganasanMorphAnalyzer:
    def __init__(self):
        # Инициализация словарей и правил
        self.load_noun_paradigms()
        self.load_verb_paradigms()
        self.load_pronoun_paradigms()
        self.load_numeral_paradigms()

    def load_noun_paradigms(self):
        """Загрузка парадигм склонения существительных."""
        # Суффиксы падежей для 3 склонений
        self.noun_declensions = {
            1: {  # 1 склонение (основа на долгий гласный или дифтонг)
                'nom': '', 'gen': '', 'acc': '',
                'dat': {
                    'sg': ['те', 'дя'],
                    'dl': ['гайте', 'гайдя'],
                    'pl': ['нти', 'дя']
                },
                'loc': {
                    'sg': ['тены', 'нану'],
                    'dl': ['гайтены', 'гайнану'],
                    'pl': ['тини', 'нану']
                },
                'abl': {
                    'sg': ['гате'],
                    'dl': ['гайгате'],
                    'pl': ['гите']
                },
                'prol': {
                    'sg': ['ниимэны', 'ниизэ'],
                    'dl': ['гайниимэны', 'гайниизэ'],
                    'pl': ['ниимэны', 'ниизэ']
                }
            },
            2: {  # 2 склонение
                'nom': '', 'gen': '', 'acc': '',
                'dat': {
                    'sg': ['нтэ', 'дя'],
                    'dl': ['гайтэ', 'гайдя'],
                    'pl': ['нти', 'дя']
                },
                'loc': {
                    'sg': ['нану', 'тэны'],
                    'dl': ['гайнану', 'гайтэны'],
                    'pl': ['нану', 'тини']
                },
                'abl': {
                    'sg': ['гатэ'],
                    'dl': ['гайгатэ'],
                    'pl': ['гитэ']
                },
                'prol': {
                    'sg': ['ниимэны', 'ниизэ'],
                    'dl': ['гайниимэны', 'гайниизэ'],
                    'pl': ['ниимэны', 'ниизэ']
                }
            },
            3: {  # 3 склонение (основа на согласный)
                'nom': '', 'gen': '', 'acc': {'pl': 'й'},
                'dat': {
                    'sg': ['те', 'дя'],
                    'dl': ['кайте', 'кайдя'],
                    'pl': ['йти', 'дя']
                },
                'loc': {
                    'sg': ['нану', 'тены'],
                    'dl': ['кайнану', 'кайтены'],
                    'pl': ['нану', 'йтини']
                },
                'abl': {
                    'sg': ['кате'],
                    'dl': ['кайгате'],
                    'pl': ['гите']
                },
                'prol': {
                    'sg': ['ниимэны', 'нинўэ'],
                    'dl': ['кайниимэны', 'кайнинўэ'],
                    'pl': ['ниимэны', 'нинўэ']
                }
            }
        }

        # Лично-притяжательные суффиксы
        self.possession_suffixes = {
            'sg': {'1': 'мё', '2': 'рё', '3': 'зы'},
            'dl': {'1': 'ми', '2': 'ри', '3': 'зи'},
            'pl': {'1': 'мы"', '2': 'ры"', '3': 'зы'}
        }

        # Чередования согласных
        self.consonant_alternations = {
            'к-г': ('к', 'г'), 'г-к': ('г', 'к'), 'х-б': ('х', 'б'),
            'т-з': ('т', 'з'), 'з-т': ('з', 'т'), '"-з': ('"', 'з'),
            '"-й': ('"', 'й'), 'з-с': ('з', 'с'), 'н-н': ('н', 'н'),
            'н-н': ('н', 'н'), 'с-д': ('с', 'д'), 'с-д': ('с', 'д'),
            'нд-нт': ('нд', 'нт'), 'нт-нд': ('нт', 'нд'), 'нс-нд': ('нс', 'нд'),
            'нд-нс': ('нд', 'нс'), 'нс-нд': ('нс', 'нд'), 'нг-нк': ('нг', 'нк'),
            'нк-нг': ('нк', 'нг'), 'нх-мб': ('нх', 'мб')
        }

    def load_verb_paradigms(self):
        """Загрузка парадигм спряжения глаголов."""
        # Личные окончания для разных типов спряжения
        self.verb_conjugations = {
            'subjective': {  # Субъектное спряжение
                'pres': {
                    'sg': {'1': 'м', '2': 'н', '3': ''},
                    'dl': {'1': 'ми', '2': 'ри', '3': 'гай'},
                    'pl': {'1': 'му"', '2': 'ру"', '3': '"'}
                },
                'past': {
                    'sg': {'1': 'м', '2': 'н', '3': ''},
                    'dl': {'1': 'ми', '2': 'ри', '3': 'гай'},
                    'pl': {'1': 'мы"', '2': 'ры"', '3': '"'}
                },
                'fut': {
                    'sg': {'1': 'м', '2': 'н', '3': ''},
                    'dl': {'1': 'ми', '2': 'ри', '3': 'гай'},
                    'pl': {'1': 'му"', '2': 'ру"', '3': '"'}
                }
            },
            'subj_obj': {  # Субъектно-объектное спряжение
                'sg_obj': {
                    'sg': {'1': 'мə', '2': 'рə', '3': 'ту'},
                    'dl': {'1': 'ми', '2': 'ри', '3': 'зи'},
                    'pl': {'1': 'му"', '2': 'ру"', '3': 'зун'}
                },
                'dl_obj': {
                    'sg': {'1': 'не', '2': 'те', '3': 'ту'},
                    'dl': {'1': 'ни', '2': 'ти', '3': 'ти'},
                    'pl': {'1': 'ну"', '2': 'ту"', '3': 'тун'}
                },
                'pl_obj': {
                    'sg': {'1': 'ня', '2': 'тя', '3': 'ту'},
                    'dl': {'1': 'ни', '2': 'ти', '3': 'ти'},
                    'pl': {'1': 'ну"', '2': 'ту"', '3': 'тун'}
                }
            },
            'subj_nonobj': {  # Субъектно-безобъектное спряжение
                'pres': {
                    'sg': {'1': 'нə', '2': 'н', '3': 'зə'},
                    'dl': {'1': 'ни', '2': 'ти', '3': 'ти'},
                    'pl': {'1': 'ну"', '2': 'ту"', '3': 'тə'}
                }
            }
        }

        # Временные суффиксы
        self.tense_suffixes = {
            'pres': {'dur': 'ту', 'mom': '"а'},
            'past': {'dur': 'дуо', 'mom': 'диэ'},
            'fut': {'dur': '"сузэ', 'mom': '"сызэ'}
        }

        # Наклонения
        self.moods = {
            'imperative': {
                'sg': {'2': '"', '3': ''},
                'dl': {'2': 'ри', '3': 'гай'},
                'pl': {'2': 'ру"', '3': '"'}
            },
            'optative': {
                'sg': {'1': 'гуом', '2': 'гуон', '3': 'гуо'},
                'dl': {'1': 'гуоми', '2': 'гуори', '3': 'гуогай'},
                'pl': {'1': 'гуому"', '2': 'гуору"', '3': 'гуо"'}
            },
            'conditional': {
                'sg': {'1': 'буазом', '2': 'буазон', '3': 'буазо'},
                'dl': {'1': 'буазоми', '2': 'буазори', '3': 'буазогай'},
                'pl': {'1': 'буазому"', '2': 'буазору"', '3': 'буазо"'}
            }
        }

    def load_pronoun_paradigms(self):
        """Загрузка парадигм местоимений."""
        self.pronouns = {
            'personal': {
                'sg': {'1': 'мәне', '2': 'тәне', '3': 'сыты'},
                'dl': {'1': 'ми', '2': 'ти', '3': 'сыти'},
                'pl': {'1': 'мын', '2': 'тын', '3': 'сытын'}
            },
            'reflexive': {
                'sg': {'1': 'нонәне', '2': 'нонәнте', '3': 'нонәнту'},
                'dl': {'1': 'нонәни', '2': 'нонәнти', '3': 'нонәнти'},
                'pl': {'1': 'нонәну"', '2': 'нонәнту"', '3': 'нонәнтун'}
            },
            'demonstrative': {
                'proximal': ['эмэ', 'эмты', 'эмэннэ'],
                'distal': ['тетти', 'тэндэ', 'таннэ'],
                'remote': ['такээ']
            },
            'interrogative': {
                'who': 'сылы?',
                'what': 'маа?',
                'which': ['курэди?', 'канкэ?', 'куннэ?', 'канемпэ?']
            }
        }

    def load_numeral_paradigms(self):
        """Загрузка парадигм числительных."""
        self.numerals = {
            'cardinal': {
                1: 'нуой', 2: 'ситти', 3: 'нагур', 4: 'теты', 5: 'сомбэ',
                6: 'мэтты', 7: 'сэйбэ', 8: 'ситтизатор', 9: 'намиайтумэ', 10: 'би"',
                11: 'би"нуой', 12: 'би"ситти', 15: 'би"сомбэ', 20: 'ситтиби"',
                50: 'сонхоби"', 100: 'дир', 1000: 'би"дир'
            },
            'ordinal': {
                1: 'неробте', 2: 'сизимти', 3: 'нагемту', 4: 'тетгемты',
                5: 'сомбэмти', 6: 'метгемты', 7: 'сэйбэмти', 8: 'ситтизатомты',
                9: 'намиайтумэмти', 10: 'би"зимти'
            },
            'other': {
                'distributive': '_мены',  # ситтимены - по два
                'collective': '_ ися',  # ситти ися - вдвоём
                'multiplicative': '_мены камеутую',  # ситтимены камеутую - двойной
                'fractional': '_ хельге'  # нагемту хельге - треть
            }
        }

    def analyze_noun(self, word):
        """Анализ существительного."""
        analysis = {'pos': 'NOUN', 'features': {}, 'stem': word}

        # Специальная обработка вопросительных слов
        if word in ['сылы?', 'маа?']:
            return {'pos': 'PRON', 'features': {'type': 'interrogative'}}

        # Проверка множественного числа с суффиксом -не"
        if word.endswith('не"'):
            analysis['features']['number'] = 'pl'
            analysis['stem'] = word[:-3]
            return analysis

        # Проверка дательно-направительного падежа с суффиксом -дэне
        if word.endswith('дэне'):
            analysis['features'].update({
                'case': 'dat',
                'number': 'sg'
            })
            analysis['stem'] = word[:-4]
            return analysis

        # Остальные проверки из предыдущей версии
        if word.endswith(('гай', 'кай')):
            analysis['features']['number'] = 'dl'
            analysis['stem'] = word[:-3]
            return analysis

        elif word.endswith('"'):
            analysis['features']['number'] = 'pl'
            analysis['stem'] = word[:-1]
            return analysis

        for num in ['sg', 'dl', 'pl']:
            for pers in ['1', '2', '3']:
                for suffix in self.possession_suffixes[num][pers]:
                    if word.endswith(suffix):
                        analysis['features'].update({
                            'possession': 'yes',
                            'possessor_num': num,
                            'possessor_pers': pers
                        })
                        analysis['stem'] = word[:-len(suffix)]
                        return analysis

        for decl in [1, 2, 3]:
            case_data = self.noun_declensions[decl]
            for case in ['dat', 'loc', 'abl', 'prol']:
                if case not in case_data:
                    continue

                suffixes = case_data[case].get('sg', [])
                if not isinstance(suffixes, list):
                    suffixes = [suffixes]

                for suffix in suffixes:
                    if word.endswith(suffix):
                        analysis['features'].update({
                            'case': case,
                            'number': 'sg',
                            'declension': decl
                        })
                        analysis['stem'] = word[:-len(suffix)]
                        return analysis

        analysis['features'].update({
            'case': 'nom',
            'number': 'sg'
        })
        return analysis

    def detect_declension(self, stem):
        """Определение склонения по основе."""
        # 3 склонение - основа на согласный
        if stem.endswith(('"', 'м', 'н', 'р', 'й')):
            return 3
        # 1 склонение - основа на долгий гласный или дифтонг
        elif re.search(r'(aa|ee|uu|yy|ai|au|ei|eu|oi|ou|ui|uu)$', stem):
            return 1
        # 2 склонение - остальные случаи
        else:
            return 2

    def detect_possession(self, word, stem):
        """Определение притяжательных суффиксов."""
        for num in ['sg', 'dl', 'pl']:
            for pers in ['1', '2', '3']:
                for suffix in self.possession_suffixes[num][pers]:
                    if word.endswith(stem + suffix):
                        return {
                            'possession': 'yes',
                            'possessor_num': num,
                            'possessor_pers': pers
                        }
        return None

    def detect_case(self, word, stem, declension, number):
        """Определение падежа по суффиксу."""
        if declension not in self.noun_declensions:
            return None

        case_data = self.noun_declensions[declension]

        for case in ['dat', 'loc', 'abl', 'prol']:
            if case not in case_data:
                continue

            suffixes = case_data[case].get(number, [])
            if not isinstance(suffixes, list):
                suffixes = [suffixes]

            for suffix in suffixes:
                if word.endswith(stem + suffix):
                    return {'case': case}

        return None

    def analyze_verb(self, word):
        """Анализ глагола (более строгая версия)."""
        analysis = {'pos': 'VERB', 'features': {}}

        # Более строгие проверки на глагол

        # 1. Проверка временных суффиксов
        found_tense = False
        for tense in ['pres', 'past', 'fut']:
            for aspect in ['dur', 'mom']:
                suffix = self.tense_suffixes[tense][aspect]
                if suffix in word:
                    analysis['features']['tense'] = tense
                    found_tense = True
                    break
            if found_tense:
                break

        if not found_tense:
            # Если нет временного суффикса, вероятно, это не глагол
            analysis['pos'] = 'UNKN'
            return analysis

        # 2. Проверка личных окончаний
        person_num = self.detect_person_number(word, None, None)
        if not person_num:
            analysis['pos'] = 'UNKN'
            return analysis

        analysis['features'].update(person_num)

        # 3. Проверка типа спряжения
        conjugation_type = self.detect_conjugation_type(word)
        if not conjugation_type:
            analysis['pos'] = 'UNKN'
            return analysis

        analysis['features']['conjugation'] = conjugation_type

        # 4. Проверка наклонения
        mood = self.detect_mood(word)
        if mood:
            analysis['features']['mood'] = mood

        # 5. Добавление основы
        stem = self.extract_stem(word, analysis['features'])
        if stem:
            analysis['stem'] = stem

        return analysis

    def detect_conjugation_type(self, word):
        """Определение типа спряжения."""
        # Проверка субъектно-объектного спряжения
        for obj_type in ['sg_obj', 'dl_obj', 'pl_obj']:
            for num in ['sg', 'dl', 'pl']:
                for pers in ['1', '2', '3']:
                    suffix = self.verb_conjugations['subj_obj'][obj_type][num][pers]
                    if word.endswith(suffix):
                        return f'subj_obj_{obj_type}'

        # Проверка субъектно-безобъектного спряжения
        for num in ['sg', 'dl', 'pl']:
            for pers in ['1', '2', '3']:
                suffix = self.verb_conjugations['subj_nonobj']['pres'][num][pers]
                if word.endswith(suffix):
                    return 'subj_nonobj'

        # По умолчанию - субъектное спряжение
        return 'subjective'

    def detect_tense(self, word):
        """Определение времени глагола."""
        for tense in ['pres', 'past', 'fut']:
            for aspect in ['dur', 'mom']:
                suffix = self.tense_suffixes[tense][aspect]
                if suffix in word:
                    return tense
        return None

    def detect_mood(self, word):
        """Определение наклонения глагола."""
        for mood in ['imperative', 'optative', 'conditional']:
            for num in ['sg', 'dl', 'pl']:
                for pers in ['1', '2', '3']:
                    if pers not in self.moods[mood][num]:
                        continue
                    suffix = self.moods[mood][num][pers]
                    if word.endswith(suffix):
                        return mood
        return None

    def detect_person_number(self, word, conjugation_type=None, mood=None):
        """Определение лица и числа глагола."""
        if not conjugation_type:
            conjugation_type = self.detect_conjugation_type(word)

        if not mood:
            mood = self.detect_mood(word) or 'indicative'

        # Для каждого типа спряжения и наклонения свои парадигмы
        if mood == 'indicative':
            if conjugation_type.startswith('subj_obj'):
                obj_type = conjugation_type.split('_')[-1]
                for num in ['sg', 'dl', 'pl']:
                    for pers in ['1', '2', '3']:
                        suffix = self.verb_conjugations['subj_obj'][obj_type][num][pers]
                        if word.endswith(suffix):
                            return {'person': pers, 'number': num}
            elif conjugation_type == 'subj_nonobj':
                for num in ['sg', 'dl', 'pl']:
                    for pers in ['1', '2', '3']:
                        suffix = self.verb_conjugations['subj_nonobj']['pres'][num][pers]
                        if word.endswith(suffix):
                            return {'person': pers, 'number': num}
            else:  # subjective
                for num in ['sg', 'dl', 'pl']:
                    for pers in ['1', '2', '3']:
                        for tense in ['pres', 'past', 'fut']:
                            suffix = self.verb_conjugations['subjective'][tense][num][pers]
                            if word.endswith(suffix):
                                return {'person': pers, 'number': num}
        else:  # не изъявительное наклонение
            for num in ['sg', 'dl', 'pl']:
                for pers in ['1', '2', '3']:
                    if pers not in self.moods[mood][num]:
                        continue
                    suffix = self.moods[mood][num][pers]
                    if word.endswith(suffix):
                        return {'person': pers, 'number': num}

        return None

    def detect_aspect(self, word):
        """Определение вида глагола (совершенный/несовершенный)."""
        # Несовершенный вид часто имеет суффиксы -ты, -ти, -ту
        if re.search(r'(ты|ти|ту)[мнр]?[ёэыу]?["]?$', word):
            return 'imperfective'
        # Совершенный вид часто имеет гортанную смычку
        elif '"' in word[-3:]:
            return 'perfective'
        return None

    def detect_voice(self, word):
        """Определение залога глагола."""
        # Возвратные глаголы часто оканчиваются на -зэ
        if word.endswith('зэ'):
            return 'reflexive'
        return 'active'

    def extract_stem(self, word, features):
        """Извлечение основы глагола."""
        conjugation = features.get('conjugation')
        mood = features.get('mood', 'indicative')
        person = features.get('person')
        number = features.get('number')

        if not all([conjugation, person, number]):
            return None

        # Для изъявительного наклонения
        if mood == 'indicative':
            if conjugation.startswith('subj_obj'):
                obj_type = conjugation.split('_')[-1]
                suffix = self.verb_conjugations['subj_obj'][obj_type][number][person]
            elif conjugation == 'subj_nonobj':
                suffix = self.verb_conjugations['subj_nonobj']['pres'][number][person]
            else:  # subjective
                tense = features.get('tense', 'pres')
                suffix = self.verb_conjugations['subjective'][tense][number][person]
        else:  # не изъявительное наклонение
            suffix = self.moods[mood][number][person]

        if word.endswith(suffix):
            return word[:-len(suffix)]
        return None

    def analyze_pronoun(self, word):
        """Анализ местоимения."""
        analysis = {'pos': 'PRON', 'features': {}}

        # Проверка личных местоимений
        for num in ['sg', 'dl', 'pl']:
            for pers in ['1', '2', '3']:
                if word == self.pronouns['personal'][num][pers]:
                    analysis['features'].update({
                        'type': 'personal',
                        'person': pers,
                        'number': num
                    })
                    return analysis

        # Проверка возвратных местоимений
        for num in ['sg', 'dl', 'pl']:
            for pers in ['1', '2', '3']:
                if word == self.pronouns['reflexive'][num][pers]:
                    analysis['features'].update({
                        'type': 'reflexive',
                        'person': pers,
                        'number': num
                    })
                    return analysis

        # Проверка указательных местоимений
        for subtype in ['proximal', 'distal', 'remote']:
            if word in self.pronouns['demonstrative'][subtype]:
                analysis['features'].update({
                    'type': 'demonstrative',
                    'subtype': subtype
                })
                return analysis

        # Проверка вопросительных местоимений
        if word in [self.pronouns['interrogative']['who'],
                    self.pronouns['interrogative']['what']]:
            analysis['features'].update({
                'type': 'interrogative',
                'subtype': 'who' if word == 'сылы?' else 'what'
            })
            return analysis

        for which_pronoun in self.pronouns['interrogative']['which']:
            if word == which_pronoun:
                analysis['features'].update({
                    'type': 'interrogative',
                    'subtype': 'which'
                })
                return analysis

        # Если не распознано, отмечаем как местоимение без дополнительных признаков
        analysis['features']['type'] = 'unknown'
        return analysis

    def analyze_numeral(self, word):
        """Анализ числительного."""
        analysis = {'pos': 'NUM', 'features': {}}

        # Проверка количественных числительных
        for num, form in self.numerals['cardinal'].items():
            if word == form:
                analysis['features'].update({
                    'type': 'cardinal',
                    'value': num
                })
                return analysis

        # Проверка порядковых числительных
        for num, form in self.numerals['ordinal'].items():
            if word == form:
                analysis['features'].update({
                    'type': 'ordinal',
                    'value': num
                })
                return analysis

        # Проверка других типов числительных
        for num in self.numerals['cardinal'].values():
            for subtype, pattern in self.numerals['other'].items():
                if word == num + pattern:
                    analysis['features'].update({
                        'type': subtype,
                        'value': next(k for k, v in self.numerals['cardinal'].items() if v == num)
                    })
                    return analysis

        # Если не распознано, отмечаем как числительное без дополнительных признаков
        analysis['features']['type'] = 'unknown'
        return analysis

    def analyze(self, word):
        """Основной метод анализа слова."""
        # Удаление вопросительного знака, если есть
        clean_word = word.rstrip('?')

        # Измененный порядок проверки частей речи:
        # 1. Сначала проверяем числительные (они имеют четкие формы)
        num_analysis = self.analyze_numeral(clean_word)
        if num_analysis['features'].get('type') != 'unknown':
            return num_analysis

        # 2. Проверяем местоимения (они тоже имеют четкие формы)
        pron_analysis = self.analyze_pronoun(clean_word)
        if pron_analysis['features'].get('type') != 'unknown':
            return pron_analysis

        # 3. Проверяем существительные (более строгая проверка)
        noun_analysis = self.analyze_noun(clean_word)
        # Проверяем, есть ли признаки существительного
        if ('case' in noun_analysis['features'] or
                'number' in noun_analysis['features'] or
                'declension' in noun_analysis['features']):
            return noun_analysis

        # 4. Только если не распознано как другие части речи, проверяем глагол
        verb_analysis = self.analyze_verb(clean_word)
        # Проверяем, есть ли признаки глагола
        if ('conjugation' in verb_analysis['features'] or
                'tense' in verb_analysis['features'] or
                'mood' in verb_analysis['features']):
            return verb_analysis

        # 5. Если не распознано, возвращаем анализ как существительное (по умолчанию)
        return noun_analysis


if __name__ == "__main__":
    analyzer = NganasanMorphAnalyzer()

    # Тестовые слова для анализа
    test_words = [
        "таа",      # олень (сущ. ед.ч.)
        "таагай",   # два оленя
        "таане",    # олени
        "десьмё",   # мой отец
        "дедитэне", # к моему отцу
        'ту"ом',    # я пришел (глагол)
        "туйсузәм", # я приду
        "мәне",     # я (мест.)
        "ситти",    # два (числ.)
        "сылы?",    # кто? (вопр. мест.)
        "нонәнте"   # ты сам (возвр. мест.)
    ]

    # Анализ и вывод результатов
    for word in test_words:
        analysis = analyzer.analyze(word)
        print(f"Слово: {word}")
        print("Анализ:")
        for key, value in analysis.items():
            print(f"  {key}: {value}")
        print()

from stanfordcorenlp import StanfordCoreNLP
from deeppavlov import build_model

# Загрузка модели зависимостей
model = build_model("ru_syntagrus_joint_parsing")

# Текст для анализа
text = "Мама мыла раму."

# Выполнение анализа зависимостей
result = model([text])

# Извлечение результатов
dependencies = result[0][0]['syntax_dep_tree']

# Вывод результатов
for dep in dependencies:
    print(f"Head: {dep['head']}, Dependent: {dep['dep']}, Relation: {dep['link']}")
def build_syntax_tree(text):
    # Установка пути к файлу JAR Stanford CoreNLP
    # Замените путь на соответствующий путь на вашей системе
    stanfordnlp.download('ru')
    stanfordnlp.Pipeline(processors='tokenize,lemma,pos')
    nlp = StanfordCoreNLP('<путь_к_файлу_jar_stanford_corenlp>')

    # Определение параметров анализа
    props = {
        'annotators': 'parse',
        'pipelineLanguage': 'en',
        'outputFormat': 'json'
    }

    # Анализ текста и получение результатов
    result = nlp.annotate(text, properties=props)
    syntax_tree = result['sentences'][0]['parse']

    # Закрытие соединения с сервером Stanford CoreNLP
    nlp.close()

    return syntax_tree
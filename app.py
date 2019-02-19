"""Приложение извлекает из текста именованные сущности."""

# todo: Библиотека natasha "из коробки" находит сущности не очень качественно.
# todo: Ее надо дополнительно настраивать.


from flask import Flask, request, jsonify
from natasha import (
    NamesExtractor,
    AddressExtractor,
    DatesExtractor,
    MoneyExtractor
)

app = Flask(__name__)


names_extractor = NamesExtractor()
address_extractor = AddressExtractor()
dates_extractor = DatesExtractor()
money_extractor = MoneyExtractor()


def find_named_entities(ner_extractor, text):
    """Находит именованные сущности в тексте.

    :param ner_extractor: объект класса NamesExtractor, AddressExtractor,
    DatesExtractor или MoneyExtractor
    :param text: str
    :return: list of namedtuples
    """
    matches = ner_extractor(text)
    return [_.fact.as_json for _ in matches]


def get_response(text):
    """Находит именованные сущности в тексте.

    :param text: str
    :return: list of namedtuple
    """
    names = find_named_entities(names_extractor, text)
    addresses = find_named_entities(address_extractor, text)
    dates = find_named_entities(dates_extractor, text)  # todo: разобраться с parts
    money = find_named_entities(money_extractor, text)
    response = {
        'names': names,
        'addresses': addresses,
        'dates': dates,
        'money': money,
        'text': text
    }
    return response


@app.route('/', methods=['POST'])
def ner():
    """Находит именованые сущности в тексте.

    В теле запроса принимает текст.
    :return: json
    """
    text = request.data.decode()
    response = get_response(text)
    return jsonify(response)


if __name__ == '__main__':
    app.run()

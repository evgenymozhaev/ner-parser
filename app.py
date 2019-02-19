"""Приложение извлекает из текста именованные сущности."""

# todo: Библиотека natasha "из коробки" находит сущности не очень качественно.
# todo: Ее надо дополнительно настраивать.


from flask import Flask, request, jsonify
from natasha import (
    NamesExtractor,
    AddressExtractor,
    DatesExtractor,
    MoneyExtractor,
    LocationExtractor
)

app = Flask(__name__)

# todo: LocationExtractor работает плохо, его надо настравиать,
# todo: но он умеет находить города, страны и регионы.
# todo: AddressExtractor лучше находит и представляет города,
# todo: но не находит страны и регионы. Он находит улицы и дома,
# todo: нужно исключить их из выдачи и объединить результаты с
# todo: результатами LocationExtractor-а.

names_extractor = NamesExtractor()
address_extractor = AddressExtractor()
dates_extractor = DatesExtractor()
money_extractor = MoneyExtractor()
location_extractor = LocationExtractor()


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
    locations = find_named_entities(location_extractor, text)
    response = {
        'names': names,
        'addresses': addresses,
        'dates': dates,
        'money': money,
        'locations': locations,
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

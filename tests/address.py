import requests
from data.endpoints import find_address
from helpers.auth_helpers import get_auth, confirm_auth, get_token
from config import host


session = {}

get_auth(session)
confirm_auth(session)
get_token(session)

# Если это тест - у него должно быть именование по стилю pytest
def test_get_address():
	# Название улицы лучше сразу вынести в отдельную перменную в модуль data
	# Потом адреса нам могут еще пригодиться, лучше  сразу брать из одного места
    data = {'SearchTerm': 'г Казань ул Чистопольская 11', 'MaxCount': 5}
    print(host + find_address)
    #Когда передаешь json нельзя просто использовать data=data, где data это словарь.
    # У меня так запрос не доходит
    # Есть два варианта
    # r = requests.post(host + find_address, json=data, ...
    # r = requests.post(host + find_address, data=str(data).encode('utf-8'), ...
    r = requests.post(host + find_address, json=data, headers={'SessionToken': session['SessionToken'],
                                                               'Content-Type': 'application/json; charset=utf-8',
                                                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 OPR/71.0.3770.138 (Edition Yx GX)'
                                                              })
    assert r.status_code == 200 # в уроке 2 эту проверку вынести в параметризованный запрос
    assert r.json()['Result'][0]['StreetFias'] == "63b26927-9a86-4b80-bba9-02b37135c686", "Запрос на получение адреса не прошел или fias сменился "
    assert r.json()['Result'][0]['House'] == "11"
    assert r.json()['Result'][0]['Value'] == "г Казань, ул Чистопольская, д 11"
    assert r.json()['Result'][0]['Granularity'] == 8


test_get_address()

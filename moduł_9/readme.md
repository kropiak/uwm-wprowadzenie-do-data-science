# Moduł 8 - Pakiet `requests` i żądania protokołu HTTP. Wybrane funkcje wbudowane.

## 1. Pakiet `requests`.

Pakiet requests pozwala na wysyłanie żądań HTTP i obsługę odpowiedzi tego protokołu. Dzięki temu możemy pobrać np. źródło wybranej strony WWW lub odpytywać API, które zwraca dane np. w formacie json.

Aby skorzystać z pakietu `requests` musimy najpierw go zainstalować i zaimportować.

**Listing 1**
```console
pip install requests
# lub
python -m pip install requests
```

Poniżej przykład żądania i odpowiedzi, jaka została zwrócona.

**Listing 2**
```python
import requests

response = requests.get('https://api.github.com')
# obiekt response
print(response)

# kod statusu
print(response.status_code)

# strumień bajtów
print(response.content)
# tekst odpowiedzi jako str
print(response.text)
# odpowiedź w formacie json - jeżeli to możliwe 
print(response.json())
# nagłówki
print(response.headers)
```

Rzeczywista obsługa żądania będzie zapewne zaimplementowana w bardziej wyrafinowany sposób, np. z obsługą błędów.

**Listing 3**
```python
import requests
from requests.exceptions import HTTPError

for url in ['https://api.github.com', 'https://api.github.com/invalid']:
    try:
        response = requests.get(url)

        # wyjątek nie zostanie zgłoszony jeżeli status == OK
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'Błąd HTTP: {http_err}')
    except Exception as err:
        print(f'Inny wyjątek: {err}')
    else:
        print('OK!')
```

Przykład z odpytaniem serwisu openweather.com. 


**Listing 4**
```python
api_key = '<tu klucz z API>'
city = 'Olsztyn'

# poniższy url służy do odpytania API o szczegóły geo dla danego miasta
# te informacje, a konkretnie lat i len
url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}'
response = requests.get(url)
print(response.json())

# jeżeli chcemy przekazywać parametry za pomocą mechanizmu dosatrczonego przez requests
# możemy to zrobić następująco

response = requests.get(
    'http://api.openweathermap.org/geo/1.0/direct',
    params={'city': city, 'limit': 5, 'api_key': api_key}
)

```

Dane wyjściowe są dość obszerne, ale format nie powinien być już obcy. Aby odpytać to API o dane pogodowe, potrzebna jest szerokość i długość geograficzna danego punktu. Te dane znajdują się w odpowiedzi z żądania przedstawionego powyżej.


Zapytanie o dane pogodowe odbywa się do innego adresu.

Przykład:

https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}

Szczegóły znajdują się pod adresem: https://openweathermap.org/current

Pakiet `requests` umożliwia również wysyłanie innych typów żadań, autentykacji czy utrzymywania sesji z odległym serwerem. Opis tych zagadnień można znaleźć tu:
* https://pypi.org/project/requests/
* https://realpython.com/python-requests/

### Rozwiązanie do zaimplementowania.

1. Potrzebujemy funkcji, która po przekazaniu nazwy miasta zwróci parametry `lon` i `lat` niezbędne do pobrania danych pogodowych.
2. Kolejna funkcja odpyta API o dane pogodowe dla pobranych wcześniej parametrów danego miasta.
3. Aby całość nieco zoptymalizować i nie wysyłać żądania do API o parametry `lon` i `lat` za każdym razem, powinniśmy zaimplementować rozwiązanie, które przed wysłaniem zapytania o nie, sprawdzi, czy dane znajdują się lokalnie, w przygotowanym pliku (format json). Dane do tego pliku powinny być zapisywane po pierwszym odpytaniu o parametry `lon` i `lat`.

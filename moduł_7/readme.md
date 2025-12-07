# Moduł 7 - Zarządzanie pakietami.

## 1. Zarządzanie pakietami.

Właściwie każdy popularny język programowania posiada mechanizm pozwalający na zarządzanie dodatkowymi bibliotekami czy pakietami. Python również posiada swojego menadżera pakietów o nazwie `pip`. W wersji 3.x nie jest konieczne jego ręczne instalowanie, gdyż jest już domyślnie dołączany do tych dystrybucji.


Aby korzystać z narzędzia `pip` w wierszu poleceń systemu Windows musimy się najpierw upewnić, że interpreter Pythona (oraz folder `Scripts`) znajduje się w zmiennej środowiskowej `PATH`. Możemy albo wyświetlić zmienną `PATH`, albo po prostu w terminalu wykonać polecenie `python -V`, które zwróci wersję Pythona, z której aktualnie korzystamy lub polecenie nie zostanie rozpoznane.

Jeżeli powyższy warunek jest spełniony możemy uruchomić narzędzie `pip` i np. wyświetlić listę pakietów z aktualnego środowiska Pythona:
```console
python –m pip list
# lub
py -m pip list
# lub
pip list
```

Listę poleceń i skromny help uzyskamy po komendzie:
```console
python –m pip help
```

Index pakietów, które można zainstalować z indexy PyPi znajdziemy pod adresem https://pypi.python.org/pypi, gdzie aktualnie znajduje się ponad 500 000 pakietów…

Jak wynika z helpa komenda służąca do instalacji pakietu to `install nazwa_pakietu`. Zainstalujmy pakiet `requests`.
```console
python –m pip install requests
```

Możliwe jest również wybranie konkretnej wersji pakietu, którą chcemy zainstalować.
Jak nie trudno się domyślić opcja uninstall służy do odinstalowywania pakietów.

Narzędzie `pip` umożliwia również instalowanie pakietów na podstawie pliku wymagań, którego przykładowa postać może wyglądać tak:

```txt
# ####### example-requirements.txt ####### 
# ###### wymagania bez określonej wersji ###### 
nose
nose-cov
beautifulsoup4 

###### wymagania z okresloną wersją ###### 
# zobacz https://www.python.org/dev/peps/pep-0440/#version-specifiers 
docopt == 0.6.1 
# dopasowanie wersji. Musi być 0.6.1 
keyring >= 4.1.1 
# minimalna wersja 4.1.1 
coverage != 3.5 
# wykluczenie wersji. Wszystko poza wersją 3.5 
Mopidy-Dirble ~= 1.1 
# Kompatybilna wersja. Rozumiane jako >= 1.1, == 1.* 
# ###### odwołuje się do innego pliku z wymaganiami ###### 
-r other-requirements.txt 
# 
# 
###### konkretny plik z pakietem np. wcześniej pobrany ###### 
./downloads/numpy-1.9.2-cp34-none-win32.whl http://wxpython.org/Phoenix/snapshot-builds/wxPython_Phoenix-3.0.3.dev1820+49a8884-cp34-none-win_amd64.whl 
# 
###### dodatkowe pakiety bez określania wersji ###### 
# Umieszczone tutaj tylko po to, aby pokazać, że kolejność nie ma znaczenia. 
rejected 
green 
#
```
Komenda uruchamiająca instalację pakietów z pliku requirements.txt:
```console
python –m pip install –r requirements.txt
```

Możliwe jest też dość łatwe zapisanie aktualnie zainstalowanych modułów do pliku za popśrednictwem narzędzia pip oraz przekierowania strumienia bajtów:

```console
pip freeze > requirements.txt

# przykładowa zawartość pliku
simplejson==3.19.3
sqlparse==0.5.1
tzdata==2024.2
uritemplate==4.1.1
urllib3==2.2.3
```

Są to podstawowe i najczęściej wykorzystywane komendy narzędzia PIP. Po bardziej szczegółową dokumentację wraz z przykładami odsyłam pod adres: https://pip.pypa.io/en/stable/.

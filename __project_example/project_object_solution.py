class Dataset:
    """
    Przykładowa klasa o nazwie Dataset, w ramach której umieszczono część metod opisanych w wymaganiach projektu
    """

    # Jedna z metod magicznych (tak nazywają się te, których nazwy rozpoczynają się i kończą
    # znakami __, ta jest wykonywana w momencie tworzenia nowego obiektu z klasy Dataset,
    # tę metodę nazywamy konstruktorem. W tej metoddzie inicjalizujemy (definiujemy oraz przypisujemy wartość
    # po raz pierwszy w cyklu życia obiektu) zmienne obiektu (self.), które są współdzielone pomiędzy
    # wszystkie metody klasy, co ułatwia wymianę danych między nimi w porównaniu z rozwiązaniem
    # bazującym tylko na funkcjach.
    def __init__(self):
        self.data = []
        self.labels = []
        self.class_column_index = None

    def read_data(self, filepath: str, header=True, delimiter=',', class_col_index=-1, encoding="utf-8"):
        """
        :param filepath: ścieżka do pliku z danymi
        :param header: czy w pierwszej linii pliku z danymi znajdują się nazwy kolumn (etykiety kolumn)
        :param delimiter: ogranicznik pola w pliku z danymi, separator, który oddziela dane w wierszu
        :param class_col_index: indeks kolumny, który zawiera etykiety/klasy, domyślnie ostatnia kolumna
        :param encoding: kodowanie pliku, domyślnie UTF-8
        :return: None
        """
        self.class_column_index = class_col_index

        try:
            with open(filepath, encoding=encoding) as filehandler:
                for line_idx, line in enumerate(filehandler):
                    if line_idx == 0 and header:
                        self.labels.append(line.split(delimiter))
                    else:
                        self.data.append(line.split(delimiter))
                    # inne możliwe rozwiązanie tego samego zadania
                    # for line_idx, line in enumerate(filehandler):
                    #         self.data.append(line.split(delimiter))
                    # if header:
                    #     self.labels = self.data[0]
                    #     self.data = self.data[1:]
        except IOError as err:
            print(f"Błąd odczytu pliku z danymi: {err}")

    # z wymagań to punkt: Wypisanie etykiet
    def get_labels(self) -> list[str]:
        """
        Metoda, która zwraca nagłówki kolumn datasetu, można je później wypisać lub przekazać dalej
        :return: lista nazw kolumn zbioru danych
        """
        return self.labels

    # z wymagań to punkt: Wypisz liczbę klas decyzyjnych
    def get_number_of_classes(self):
        """
        Metoda zwraca liczbę klas decyzyjnych, czyli zakładamy, że dane są dedykowane klasyfikacji lub regresji, więc
        algorytmom uczenia nadzorowanego (z etykietami opisującymi daną obserwację). Aby ułatwić cały proces przy
        wczytywaniu zbioru danych określiłem również parametr, wskazujący na indeks kolumny, który zawiera tę etykietę/klasę
        :return:
        """
        # na tym etapie dane wynikowe możemy przechowywać w słowniku, { etykieta: liczebność"
        # ostatecznie zwrócimy je jako listę krotek, zgodnie z wymaganiami
        class_counts = {}

        # iterujemy (przechodzimy element po elemencie) przez "kolumnę", którą wskazaliśmy jako zawierającą klasę decyzyjną
        # self.data ma postać listy dwupoziomowej: [[kolumna_1, kolumna_2, ... ]], musimy więc najpierw pobierać wiersz
        # a następnie dopiero wartość z kolumny tego wiersza, w przypadku numpy można odwołać się do kolumny macierzy, tam
        # iterowanie jest nieefektywne z punktu widzenia wydajności - wiele operacji jest zoptymalizowanych do przetwarzania
        # wektorowego
        for row in self.data:
            class_name = row[self.class_column_index]
            # sprawdzamy czy taka wartość klasy jest już w słowniku
            # jeżeli tak, to dodajemy do licznika 1
            if class_name in class_counts:
                class_counts[class_name] += 1
            # jeżeli nie, to dodajemy nową pozycję w słowniki z wartością równą 1
            else:
                class_counts[class_name] = 1

        # zwracamy dane jako listę krotek
        return [(key, value) for key, value in class_counts.items()]

    def data_split(self, train_pct=0.7, test_pct=0.3, val_pct=0.0):
        """
        :param train_pct: procentowa ilość rekordów z danych, które trafią do zbioru treningowego
        :param test_pct: procentowa ilość rekordów z danych, które trafią do zbioru testowego
        :param val_pct: procentowa ilość rekordów z danych, które trafią do zbioru walidacyjnego
        :return: krotka 3-elementowa z poszczególnymi podzbiorami
        """

        # TODO: 1. suma wartości procentowych musi wynosić 1
        # TODO: 2. dane powinny być przydzielane losowo, aby uniknąć sytuacji, w której zbiór jest posortowany
        # a my dodamy do poszczególnych zbiorów obiekty, których klasy decyzyjne nie zawierają się między tymi
        # zbiorami, np. dla dołaczonego zbioru iris, dane są posortowane, więc przy domyślnym podziale do train
        # trafi 70% obiektów, więc 105 pierwszych obserwacji (50 obiektów Iris-setosa, 50 obiektów Iris-versicolor oraz 5
        # obiektów Iris-virginica, a do test tylko 45 pozostałych, więc 45 obiektów Iris-virginica co jest bardzo złym
        # pomysłem w kontekście dobrze przeprowadzonego eksperymentu Machine Learning.
        # Najlepiej gdyby losować obiekty zgodnie z rozkładem (tak można to robić np. z wykorzystaniem znanych bibliotek)
        # ale tutaj możemy dane przemieszać przed wybraniem danego podzbioru. Można to osiągnąć np. poprzez moduł random,
        # i jego funkcję shuffle() docs: https://docs.python.org/3/library/random.html#random.shuffle
        import random

        # zwróć uwagę, że dane są przetasowane w trybie in-place, to znaczy, że nie jest zwracana kopia danych w postaci
        # potasowanej, ale oryginalna zmienna przechowuje teraz dane potasowane.
        random.shuffle(self.data)

        # w takim przypadku możemy po prostu pociąć (slice) dane w odpowiedniej proporcji
        # najpierw powinniśmy ustalić wartość indeksu wycinka dla podzbioru treningowego
        # rzutowanie na integer obetnie nam część dziesiętną, a parametry wycinka muszą być integerami
        train_last_index = int(len(self.data) * train_pct)
        test_last_index = int(len(self.data) * (train_pct + test_pct))
        # a podzbiór walidacyjny to wszystko to co za indeksem test_last_index

        train_data = self.data[:train_last_index]
        test_data = self.data[train_last_index:test_last_index]
        valid_data = self.data[test_last_index:]

        return train_data, test_data, valid_data

if __name__ == "__main__":
    # tu testujemy nasz moduł
    # TODO: zauważ pojawiający się znak \n po wypisaniu danych na konsolę - to jest problem do rozwiązania
    # najlepiej na etapie ładowania danych z pliku

    ds = Dataset()
    ds.read_data('iris.csv')
    print(ds.get_labels())
    # możemy się do etykiet dostać również odwołując się do pola klasy
    print(ds.labels)
    print(ds.data)

    print(ds.get_number_of_classes())

    for subset in ds.data_split():
        print(f"Ilość elementów w zbiorze: {len(subset)}")

    for subset in ds.data_split(0.7, 0.2, 0.1):
        print(f"Ilość elementów w zbiorze: {len(subset)}")

    for subset in ds.data_split(0.8, 0.1, 0.1):
        print(f"Ilość elementów w zbiorze: {len(subset)}")

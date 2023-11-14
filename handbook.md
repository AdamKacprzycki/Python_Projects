## Wstęp i tło problemu / cel

Przedstawienie problemu klasyfikacji binarnej, z jakim się zmierzono.
Wytłumaczenie znaczenia flagi (0:1) w kontekście biznesowym lub operacyjnym.

## 2. Eksploracja i przygotowanie danych
   
•	Opis danych, w tym ilości rekordów, cech i krótkie objaśnienie każdej zmiennej.  
•	Analiza eksploracyjna danych, ukazująca niezbalansowanie klas (99:1) i jak wpływa to na modelowanie.  
•	Metody przygotowania danych, w tym kodowanie gorącojedynkowe (One-Hot Encoding) zmiennej kategorycznej

## 4. Przygotowanie do modelowania
W procesie modelowania wybrano drzewo decyzyjne ze względu na jego zdolność do obsługi nieliniowych zależności między cechami a zmienną docelową, co jest często spotykane w rzeczywistych problemach klasyfikacyjnych. Drzewa decyzyjne oferują również wysoką interpretowalność, co jest istotne w wielu aplikacjach biznesowych.

### Ważenie Klas

Z powodu wyraźnego niezbalansowania klas (stosunek 99:1) w danych, zastosowano technikę ważenia klas. Przy użyciu funkcji compute_class_weight z biblioteki sklearn.utils.class_weight obliczono wagi dla klas mniejszościowych, aby przeciwdziałać ich niedoreprezentacji. Ważenie to pozwala modelowi na bardziej sprawiedliwe traktowanie obserwacji z klasy mniejszościowej, które są dla naszego zadania kluczowe.

### Selekcja Cech

W celu optymalizacji wydajności modelu wykorzystano dwie metody selekcji cech: SelectKBest, która wybiera k cech na podstawie testów statystycznych, oraz RFE (Recursive Feature Elimination), która iteracyjnie redukuje liczbę cech, eliminując te o najmniejszym wpływie. Wybór tych technik był podyktowany chęcią redukcji wymiarowości danych i uniknięciem przeuczenia modelu na mniej istotnych zmiennych.

## 5. Dostrajanie hiperparametrów
   
Użyto RandomizedSearchCV, aby przeprowadzić losowe przeszukiwanie przestrzeni hiperparametrów z uwzględnieniem zrównoważonej walidacji krzyżowej (StratifiedKFold). Walidacja krzyżowa zapewnia, że każda klasa jest równomiernie reprezentowana w każdym podziale zestawu danych, co jest istotne przy pracy z niezbalansowanymi danymi.

Dostrajanie skupiło się na kilku kluczowych hiperparametrach drzewa decyzyjnego:

•	`criterion`: miara jakości podziału,  
•	`max_depth`: maksymalna głębokość drzewa,  
•	`max_features`: liczba cech do rozważenia przy każdym podziale,  
•	`max_leaf_nodes`: maksymalna liczba węzłów końcowych.  

## 6. Ocena modelu

Jakość modelu oceniano przy użyciu krzywej ROC oraz AUC, które są standardowymi metrykami dla problemów klasyfikacji. Krzywa ROC (Receiver Operating Characteristic) to graficzna reprezentacja zdolności klasyfikatora do odróżniania między klasami przy różnych progach klasyfikacji, a AUC (Area Under the Curve) jest miarą zdolności modelu do unikania fałszywie pozytywnych i fałszywie negatywnych klasyfikacji. W przypadku niezbalansowanych klas, AUC oferuje bardziej niuansowaną ocenę niż procent poprawnych klasyfikacji.
Dodatkowo, macierz pomyłek została zastosowana do przedstawienia liczby prawdziwie pozytywnych i prawdziwie negatywnych predykcji, jak również błędów typu I i II. Macierz ta jest szczególnie przydatna w kontekście niezbalansowanych klas, gdzie liczba poprawnych klasyfikacji w klasie mniejszościowej jest kluczowym wskaźnikiem wydajności.

## 7. Wnioski i interpretacja modelu
Analiza ważności cech, uzyskana przez atrybut feature_importances_, dostarczała wglądu w to, które cechy najbardziej przyczyniają się do podziałów dokonywanych przez model. Ważność ta pomaga zrozumieć, na co model zwraca uwagę przy podejmowaniu decyzji, co może mieć implikacje zarówno dla dalszego rozwoju modelu, jak i dla strategicznych decyzji biznesowych.
Wizualizacja drzewa decyzyjnego, realizowana za pomocą funkcji plot_tree z sklearn.tree, dostarczyła graficznego przedstawienia, jak drzewo dokonuje klasyfikacji. Zawierała ona informacje o podziałach w węzłach, klasach dominujących w liściach i ważności poszczególnych cech w różnych punktach drzewa. Taka wizualizacja jest nieoceniona, gdyż pozwala na łatwe śledzenie procesu decyzyjnego modelu i może być użyteczna przy prezentacji modelu osobom niefachowym.

## Ważenie klas - co i jak:

Ważenie klas w modelach uczenia maszynowego jest techniką stosowaną w celu korygowania niezbalansowanych zbiorów danych, gdzie liczba przykładów w jednej klasie znacznie przewyższa liczbę przykładów w innej. W kontekście modelowania drzew decyzyjnych dla klasyfikacji binarnej flagi (0:1), ważenie klas jest kluczowe ze względu na wyraźną dysproporcję między klasami — stosunek 99:1, jak zostało zauważone w danych.

### Znaczenie Ważenia Klas

Gdy klasy są niezbalansowane, model ma tendencję do faworyzowania klasy większościowej, co może prowadzić do błędnej klasyfikacji przykładów z klasy mniejszościowej. W przypadku, gdy klasyfikacja prawidłowa klasy mniejszościowej jest ważniejsza (często dotyczy to przypadków, w których klasy mniejszościowe są bardziej wartościowe lub ryzykowne, np. w medycynie lub detekcji oszustw), ważenie klas staje się kluczowym elementem modelowania.

### Jak Działa Ważenie Klas

Ważenie klas polega na przypisaniu większej wagi błędom klasyfikacji w klasie mniejszościowej, co zmusza model do przywiązywania większej uwagi do tych mniej licznych przypadków. W praktyce można to osiągnąć na kilka sposobów:
•	Statyczne ważenie klas: Przydziela się wagi na podstawie odwrotności częstości występowania klas. Na przykład, jeśli klasa mniejszościowa stanowi 1% danych, a klasa większościowa 99%, klasa mniejszościowa może otrzymać wagę 99, a większościowa 1.  
•	Dynamiczne ważenie klas: Wagi mogą być także dostosowywane dynamicznie w trakcie procesu uczenia się modelu, na przykład poprzez zastosowanie algorytmów takich jak cost-sensitive learning.  

W opisywanym modelu, compute_class_weight z pakietu sklearn automatycznie oblicza wagi na podstawie rozkładu klas w danych. Obliczone wagi są następnie przekazywane do konstruktora klasyfikatora drzewa decyzyjnego jako parametr class_weight. W praktyce oznacza to, że drzewo decyzyjne będzie "karać" się bardziej za błędne klasyfikacje przykładów z klasy mniejszościowej, skutecznie zwiększając czułość modelu na te przypadki.

### Implementacja w Modelu

W przesłanym kodzie, wagi są obliczane za pomocą:
python
`class_weights = compute_class_weight('balanced', classes = [False, True], y = df['(1:0)'])
weights = {False: class_weights[0], True: class_weights[1]}`

Te wagi są przekazywane do klasyfikatora drzewa decyzyjnego jako parametr class_weight:
python

`('clf', DecisionTreeClassifier(random_state=42, class_weight=weights))`

Dzięki temu model jest bardziej czuły na klasy mniejszościowe, co jest szczególnie ważne w aplikacjach, gdzie koszt błędu w klasyfikacji takich przykładów jest wysoki. Ważenie klas w modelu klasyfikacji binarnej flagi (0:1)jest więc kluczowym krokiem w kierunku budowy sprawiedliwego i wydajnego modelu.
Podział danych na zestaw treningowy i testowy jest standardową praktyką w uczeniu maszynowym, która umożliwia ocenę wydajności modelu na danych, których model nie widział w trakcie uczenia. Funkcja train_test_split z biblioteki scikit-learn jest używana do losowego podziału danych na zestaw treningowy i testowy.

## Stratify:

Parametr test_size

Parametr test_size=0.2 określa, że 20% danych zostanie wykorzystane jako zestaw testowy, podczas gdy pozostałe 80% danych zostanie użyte do treningu modelu. Wybór rozmiaru zestawu testowego zależy od wielkości danych i potrzeb modelu; typowe wartości to od 20% do 30%.

Parametr stratify

Parametr stratify=y jest kluczowy przy pracy z niezbalansowanymi danymi. Wskazuje on funkcji train_test_split, aby podczas dzielenia danych zachowała proporcje klas z oryginalnego zestawu danych w obu zestawach: treningowym i testowym. Oznacza to, że jeśli oryginalny zestaw danych ma stosunek klas 99:1, to po podziale, oba zestawy – treningowy i testowy – również będą miały taki sam stosunek klas.

### Dlaczego stratify jest ważne

Stosowanie stratify w przypadku niezbalansowanych danych jest krytyczne z kilku powodów:

•	Reprezentatywność: Zapewnia, że oba zestawy danych są reprezentatywne dla całego zbioru, co jest szczególnie ważne w przypadku klas mniejszościowych. Bez stratyfikacji istnieje ryzyko, że wszystkie lub większość przypadków klasy mniejszościowej może znaleźć się tylko w jednym zestawie (treningowym lub testowym), co skutkowałoby niewłaściwą oceną wydajności modelu.  
•	Dokładność oceny modelu: Umożliwia dokładniejszą ocenę modelu, ponieważ model jest testowany na danych, które odzwierciedlają rzeczywisty rozkład klas.  
•	Zapobieganie nadmiernemu dopasowaniu: Pomaga w zapobieganiu nadmiernemu dopasowaniu (overfitting) do klasy większościowej, ponieważ model musi nauczyć się rozpoznawać i generalizować wzorce dla obu klas.  

Parametr random_state 

Parametr random_state=42 jest ustawiony, aby zapewnić powtarzalność podziału. Dzięki temu każda osoba korzystająca z tego samego seeda (tutaj 42) i tego samego zbioru danych dokona identycznego podziału, co jest istotne w celu zapewnienia reprodukowalności eksperymentów.
W kontekście opisanego modelu, stosowanie parametru stratify gwarantuje, że model zostanie uczciwie oceniony, ponieważ klasy mniejszościowe będą adekwatnie reprezentowane w zestawie testowym, co jest niezbędne dla wiarygodnej oceny jego zdolności predykcyjnych.

cd.

Parametr stratify w funkcji train_test_split z biblioteki scikit-learn działa w sposób, który zapewnia, że podział danych na zestaw treningowy i testowy zachowuje proporcje klas z oryginalnego zestawu danych. W praktyce oznacza to, że jeżeli w oryginalnym zbiorze danych mamy niezbalansowane klasy, na przykład w stosunku 99% do 1%, to parametr stratify zadba o to, aby ten sam stosunek został utrzymany zarówno w zestawie treningowym, jak i testowym po podziale.
Oto jak to działa krok po kroku:

1.	Rozpoznawanie Proporcji: train_test_split bada rozkład klas w przekazanej zmiennej zależnej y. Jeżeli jest ona binarna lub wieloklasowa, funkcja identyfikuje proporcje każdej klasy.  
2.	Dziel i Zachowaj Proporcje: Podczas dzielenia danych, train_test_split dzieli każdą klasę niezależnie, zapewniając, że proporcje klas są zachowane w obu zestawach. Dla każdej klasy ustala, ile próbek powinno trafić do zestawu treningowego, a ile do testowego.  
3.	Losowe Przydzielenie: Próbki z każdej klasy są następnie losowo przydzielane do odpowiedniego zestawu zgodnie z ustalonymi proporcjami. W przypadku klasy większościowej i mniejszościowej, train_test_split losowo wybierze odpowiednią liczbę próbek z każdej klasy dla zestawu treningowego i testowego, zapewniając, że stosunek klas zostanie zachowany.  
4.	Wynikowy Podział: Rezultatem jest zestaw treningowy i testowy, które odzwierciedlają oryginalny rozkład klas, co jest szczególnie ważne w przypadku klas mniejszościowych. Bez stratyfikacji, losowy podział mógłby skutkować nierównym reprezentowaniem klas, co mogłoby wprowadzić stronniczość w procesie treningu lub oceny modelu.  
W kontekście modelu klasyfikacji binarnej, gdzie jedna klasa jest znacznie mniej liczna niż druga, stratify jest niezwykle ważne, aby zapewnić, że model będzie się uczył rozpoznawać obie klasy, a nie tylko dominującą. Zapewnia to bardziej uczciwe i rzetelne szkolenie i walidację modelu, pozwalając na bardziej wiarygodne wnioski na temat jego wydajności.  

## Selekcja cech:

Selekcja cech (feature selection) to proces wyboru podzbioru istotnych cech (zmienne niezależne) wykorzystywanych do budowy modelu. Jest to istotny krok w przetwarzaniu wstępnym danych, który może pomóc w poprawie wydajności modelu poprzez redukcję wymiarowości, usunięcie nieistotnych lub redundantnych danych, oraz może pomóc w uniknięciu nadmiernego dopasowania (overfitting). W przesłanym kodzie wykorzystano dwa algorytmy selekcji cech: SelectKBest i Recursive Feature Elimination (RFE).

### SelectKBest

SelectKBest to prosty, ale potężny algorytm selekcji cech, który wybiera cechy na podstawie statystycznych testów, które mają największe znaczenie. W przesłanym kodzie SelectKBest został użyty w połączeniu z testem statystycznym f_classif:

•	f_classif: Wykonuje analizę wariancji (ANOVA) F-testu dla każdej cechy, aby ocenić siłę związku między cechą a zmienną odpowiedzi. W przypadku danych klasyfikacyjnych F-test ocenia, czy średnie dla różnych klas są statystycznie różne.  
•	Wybór cech: SelectKBest po prostu wybiera k cech, które mają najwyższe wartości statystyki F-testu.  

W kodzie k=5 oznacza, że zostanie wybranych pięć cech, które mają największe znaczenie statystyczne w stosunku do zmiennej odpowiedzi.

### Recursive Feature Elimination (RFE)

RFE jest bardziej złożonym algorytmem, który działa przez rekurencyjne usuwanie atrybutów i budowanie modelu na pozostałych atrybutach. Jest to technika oparta na zwrotnym wyeliminowaniu, która działa w następujący sposób:

1.	Model inicjalny: Algorytm trenuje początkowy model na całym zestawie cech i oblicza ważność każdej cechy.  
2.	Eliminacja: Najmniej ważne cechy są usuwane z zestawu.  
3.	Powtarzanie: Proces jest powtarzany rekurencyjnie na coraz mniejszym zbiorze cech, aż do osiągnięcia określonej liczby cech do wyboru.  
4.	Ranking: W rezultacie każda cecha ma przypisany ranking, który określa jej ważność w modelu.  

W przesłanym kodzie, RFE jest wykorzystywany z klasyfikatorem drzewa decyzyjnego jako estymatorem, aby ocenić ważność cech. n_features_to_select=5 oznacza, że RFE będzie dążyć do wyboru pięciu najważniejszych cech.  

Zastosowanie w Modelu

Wykorzystanie obu tych metod w przeszukiwaniu siatki parametrów (RandomizedSearchCV) pozwala na ocenę, które kombinacje cech najlepiej współpracują z modelem. RandomizedSearchCV losowo wybiera kombinacje cech i parametrów modelu, trenując i oceniając model na każdej z nich, co ostatecznie prowadzi do wyboru najlepszego zestawu cech i parametrów modelu.
Dzięki selekcji cech, model jest w stanie skupić się na najbardziej informatywnych danych, co zwykle prowadzi do lepszej generalizacji i wydajności. Jest to szczególnie ważne w przypadku modeli, które mogą cierpieć na nadmierne dopasowanie z powodu nadmiaru cech, jak również dla dużych zbiorów danych, gdzie redukcja wymiarowości może znacząco zmniejszyć czas potrzebny do trenowania modelu.

### RandomSerach:

Eksperyment przeprowadzony przy użyciu RandomizedSearchCV miał na celu znalezienie optymalnego zestawu hiperparametrów dla modelu klasyfikacji binarnej opartego na drzewie decyzyjnym. Eksperyment ten składał się z kilku kluczowych komponentów:

1. RandomizedSearchCV
RandomizedSearchCV jest metodą, która wykonuje losowe przeszukiwanie hiperparametrów, wybierając losowe kombinacje z określonej przestrzeni parametrów i oceniając model przy ich użyciu. W przeciwieństwie do siatki przeszukiwania (GridSearch), która testuje wszystkie możliwe kombinacje, losowe przeszukiwanie wybiera określoną liczbę kombinacji, co zmniejsza czas obliczeniowy, zwłaszcza przy dużych przestrzeniach parametrów.
Komponenty RandomizedSearchCV

•	`pipeline`: Definiuje kroki przetwarzania danych oraz model klasyfikacji.  
•	`param_distributions`: Słownik zawierający hiperparametry do przetestowania.  
•	`scoring`: Metryka używana do oceny modelu, w tym przypadku 'roc_auc', która jest odpowiednia dla niezbalansowanych danych.  
•	`cv`: Określa strategię walidacji krzyżowej.  
•	`n_iter`: Liczba różnych kombinacji parametrów do przetestowania.  
•	`random_state`: Umożliwia powtarzalność eksperymentu. 
•	`verbose:` Steruje poziomem logów wyświetlanych podczas działania funkcji.  

## 3. StratifiedKFold

StratifiedKFold to metoda walidacji krzyżowej, która jest szczególnie użyteczna w przypadku niezbalansowanych zbiorów danych. Zapewnia, że każdy zbiór walidacyjny zawiera reprezentatywną proporcję każdej klasy, zgodnie z oryginalnym rozkładem klas.

Parametry StratifiedKFold

•	n_splits: Liczba podziałów zbioru danych na części; w tym przypadku 5, co jest standardową praktyką, zapewniającą dobrą równowagę między dokładnością a kosztem obliczeniowym.  
•	shuffle: Oznacza mieszanie danych przed podziałem, co jest istotne dla zmniejszenia wariancji i uniknięcia stronniczości w walidacji krzyżowej.  
•	random_state: Umożliwia powtarzalność eksperymentu, zapewniając, że dane są mieszane w ten sam sposób przy każdym uruchomieniu.  

4. Proces Eksperymentu
   
Podczas eksperymentu RandomizedSearchCV trenuje model z różnymi kombinacjami parametrów, przekazywanymi przez param_distributions, dla każdego podziału danych utworzonego przez StratifiedKFold. Każda kombinacja parametrów jest oceniana na podstawie średniej wartości metryki roc_auc ze wszystkich podziałów walidacyjnych.

6. Liczba Wytrenowanych Modeli
   
W eksperymencie wytrenowano n_iter * n_splits modeli, gdzie n_iter to liczba różnych kombinacji parametrów do przetestowania, a n_splits to liczba podziałów w StratifiedKFold. Jeżeli n_iter było ustawione na 10, a n_splits na 5, oznacza to, że w sumie wytrenowano 50 różnych modeli.

Podsumowanie

RandomizedSearchCV w połączeniu ze StratifiedKFold stanowi potężne narzędzie do optymalizacji modeli w uczeniu maszynowym, szczególnie w kontekście niezbalansowanych danych. Losowe przeszukiwanie umożliwia efektywne i skuteczne eksplorowanie przestrzeni hiperparametrów, podczas gdy stratyfikowana walidacja krzyżowa zapewnia, że każdy model jest uczciwie oceniany, biorąc pod uwagę proporcje klas w danych.

### FeatureImportance:

8. Wnioski i interpretacja modelu
   
W ramach oceny modelu klasyfikacyjnego, bardzo ważne jest zrozumienie, które cechy mają największy wpływ na decyzje podejmowane przez model. W drzewach decyzyjnych i innych modelach opartych na drzewach, takich jak lasy losowe (Random Forests), istotność cech (ang. feature importance) odgrywa kluczową rolę w interpretacji modelu.

Feature Importance

Istotność cech w kontekście drzew decyzyjnych jest mierzona na podstawie tego, jak skutecznie cechy te są w dzieleniu próbek na odpowiednie klasy. W drzewach decyzyjnych każdy węzeł jest punktem, w którym następuje decyzja o podziale na podstawie wartości pewnej cechy. Istotność cechy jest wyliczana w następujący sposób:

1.	Zmniejszenie Nieczystości: Dla każdego węzła w drzewie obliczana jest zmiana miary nieczystości (impurity) – takiej jak Gini impurity czy entropy – przed i po podziale. Zmniejszenie nieczystości jest miarą tego, jak dobrze dana cecha poprawia dokładność podziałów w drzewie.  
2.	Normalizacja i Sumowanie: Zmniejszenie nieczystości jest następnie sumowane dla każdej cechy i normalizowane przez całkowitą liczbę zmniejszeń nieczystości we wszystkich węzłach drzewa, dając tym samym istotność dla każdej cechy.  
3.	Wynik: Wynikiem jest wartość między 0 a 1 dla każdej cechy, gdzie 0 oznacza, że cecha nie była używana przy podejmowaniu decyzji, a 1 oznacza, że cecha doskonale przewiduje wynik.  

Interpretacja

Istotność cech pozwala zrozumieć, które zmienne wejściowe są najbardziej "informatywne" dla modelu podczas dokonywania predykcji. Na przykład, jeśli cecha ma wysoką wartość istotności, oznacza to, że miała ona duży wpływ na proces decyzyjny modelu. Cechy z niską wartością istotności nie wnosiły dużo do modelu i potencjalnie mogą być kandydatami do usunięcia w procesie optymalizacji modelu.
W praktyce, jeśli cecha ma dużą wartość istotności, to może to wskazywać, że zmienne związane z tą cechą mają duży wpływ na zmienną docelową i mogą być kluczowe w podejmowaniu decyzji.
W kontekście przesłanego kodu, istotność cech została wyliczona następująco:
python
`feature_imp = random_search.best_estimator_[-1].feature_importances_`

Tutaj best_estimator_[-1] odnosi się do ostatniego estymatora w pipeline, który jest klasyfikatorem drzewa decyzyjnego, a feature_importances_ zawiera obliczone wartości istotności dla każdej cechy.
Podsumowując, istotność cech jest istotnym narzędziem, które nie tylko pomaga w interpretacji modelu, ale także może prowadzić do lepszego zrozumienia danych i ich wpływu na problem, który model próbuje rozwiązać. W kontekście modelowania biznesowego, może to również przekładać się na lepsze zrozumienie czynników wpływających na decyzje klientów lub ryzyko operacyjne.

W kontekście drzew decyzyjnych, kryterium podziału (split criterion) to metoda wykorzystywana do wyboru cechy, która najlepiej dzieli zbiór danych na odpowiednie klasy. To kryterium ocenia jakość podziału dla każdego możliwego podziału i wybiera ten, który najlepiej poprawia czystość węzła. W przesłanym kodzie, dla klasyfikatora drzewa decyzyjnego (DecisionTreeClassifier), rozważane są trzy kryteria podziału: Gini, Entropia i Log Loss.

Gini Impurity ('gini')

•	Definicja: Kryterium nieczystości Gini jest miarą, jak często losowo wybrany element zostanie błędnie oznaczony, jeśli zostałby oznaczony losowo według rozkładu etykiet w podzbiorze.  
•	Zastosowanie: Wykorzystuje się je do minimalizacji prawdopodobieństwa błędnego klasyfikowania. Wartość nieczystości Gini wynosi 0, gdy wszystkie próbki w węźle należą do jednej klasy.  
•	Obliczanie: Nieczystość Gini dla zbioru danych można obliczyć jako 1−∑(pi2)1−∑(pi2), gdzie pipi to stosunek próbek należących do klasy ii w danym węźle.  

Entropy ('entropy')

•	Definicja: Entropia, pochodząca z teorii informacji, jest miarą niepewności, chaosu lub czystości. W kontekście drzewa decyzyjnego, jest używana do mierzenia niepewności (czystości) węzła.  
•	Zastosowanie: Węzeł z niższą entropią jest bardziej homogeniczny, czyli próbki w tym węźle są bardziej spójne z punktu widzenia klasyfikacji. Idealny podział to taki, gdzie każdy węzeł po podziale zawiera tylko próbki z jednej klasy.  
•	Obliczanie: Entropię dla węzła można obliczyć jako −∑(pilog⁡2pi)−∑(pilog2pi), gdzie pipi jest prawdopodobieństwem klasy ii w węźle.  

Log Loss ('log_loss')

•	Definicja: Log Loss, znany również jako logarytmiczna strata lub logarytmiczna funkcja kosztu, jest miarą używaną w algorytmach klasyfikacji, która ocenia prawdopodobieństwa predykcji.  
•	Zastosowanie: Chociaż nie jest to standardowe kryterium dla drzew decyzyjnych w bibliotece scikit-learn, może być używane w niektórych rozszerzeniach lub niestandardowych implementacjach. Kryterium Log Loss jest szczególnie przydatne, gdy model musi być oceniany na podstawie prawdopodobieństwa predykcji, a nie tylko na najbardziej prawdopodobnej klasyfikacji.  
•	Obliczanie: W kontekście klasyfikacji binarnej, Log Loss dla pojedynczej predykcji można obliczyć jako −ylog⁡(p)−(1−y)log⁡(1−p)−ylog(p)−(1−y)log(1−p), gdzie yy to prawdziwa etykieta, a pp to przewidziane prawdopodobieństwo, że próbka należy do klasy pozytywnej.  
Wybór między 'gini' a 'entropy' często zależy od konkretnego przypadku użycia, ponieważ w praktyce oba te kryteria często prowadzą do podobnych drzew. Jednakże 'entropy' ma tendencję do tworzenia bardziej zrównoważonych drzew, natomiast 'gini' oblicza się nieco szybciej i jest domyślnym wyborem w scikit-learn. Wybór kryterium '  






# Connect4 Game
[![License](https://img.shields.io/github/license/salalba/matplotlib)](https://github.com/SalAlba/matplotlib/blob/master/LICENSE)

This game was inspierd by GitHub Repo [src [2.1]](#Resources)

## Authors
* **Salem Albarudy** - [Website](salem-albarudy.com) | [GitHub](https://github.com/SalAlba) | [Linkedin](https://www.linkedin.com/in/salem-albarudy)


* **Pawel Dulak** - [Website](https://handyman.dulare.com/) | [GitHub](https://github.com/pdulak) | [Linkedin](https://pl.linkedin.com/in/pawel-dulak)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.


## Getting Started

### Prerequisites

+ Python >= 3.7.
+ pip3

### Installing

A step by step series of examples that tell you how to get a development env running

1. clone the repo to your local machine using

``` repo
    $ git clone https://github.com/SalAlba/games
    $ cd Games/games/python/connect4
```

2. create virtual env and run using

``` bash
    $ virtualenv  venv
    $ source venv/bin/activate
```

3. install all requirements using

``` bash
    $ pip install -r requirements.txt
```


### How To Play

``` bash
    python main.py
```

## Notes / Things you should to know


### TODO

1. Sędzia
    * zna stan planszy,
    * "woła" graczy żeby wykonali ruch - przekazuje graczowi stan planszy i możliwe do wykonania ruchy - w Twoim wypadku będzie to lista kolumn do których mozna "wrzucić" pionek jak dobrze rozumiem
    * jeśli gra się zakończyła, przekazuje każdemu graczowi "nagrodę" lub "karę"
2. Zawodnik
    * potrafi policzyć sobie hash ze stanu gry (może to robić sędzia, może sam zawodnik, nie gra roli)
    * kiedy dostanie prośbę o wykonanie ruchu (przypominam że otrzymuje wtedy stan gry i możliwe ruchy) to wybiera ruch (losowo lub z pamięci) i zapisuje na liście ruchów które wykonał w tej rundzie. Ruch to jest informacja o stanie planszy i wykonanym w tej sytuacji ruchu.
    * kiedy dostanie "karę" lub "nagrodę" to oblicza nowe wartości dla wszystkich wykonanych w tej rundzie ruchów - licząc wstecz od ostatniego do pierwszego ruchu
    * potrafi zapisać stan swojej pamięci na dysk (np. pickle) i wczytać stan pamięci


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.



## License
[![License](https://img.shields.io/github/license/salalba/matplotlib)](https://github.com/SalAlba/games/blob/master/LICENSE)

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details, Copyright 2020 © <a href="https://github.com/SalAlba/" target="_blank">Salem Albarudy</a>.



## Resources

#### 1. Books
+ [[1.1.] ](#)


#### 2. Websites
+ [[2.1.] KeithGalli | Connect4-Python](https://github.com/KeithGalli/Connect4-Python)

# Калькулятор Тома

## Постановка задачи

Из Америки за помощью обратился владелец сети небольших бакалейных
магазинов фиксированных цен по имени Том.

В прошлом году Том открыл свое дело в маленьком городишке и ему пока что
приходится делать все самому (из местных он никому не доверяет, а вся
родня - далеко), в том числе, и сидеть на кассе. Сейчас он рассчитывает
стоимость заказа в ручную, что очень неудобно, так как нужно учесть налоги
штата и скидку.

Ситуация осложняется тем, что недавно Том расширился в других штатах
(там у него как раз и живут родственники), и ему теперь нужно учитывать в
расчетах налоги других штатов.

После небольших раздумий он пришел к выводу, что ему нужно приложение с
простым пользовательским интерфейсом, тремя полями для ввода и одним
полем вывода конечной стоимости заказа - “Розничный калькулятор Тома”, как
назвал его Том.

Готовый продукт - розничный калькулятор Тома

**Три поля для ввода:**

* Количество товаров.
* Цена за товар.
* Код штата.

**Как должно работать:**

* На основе общей стоимости заказа рассчитывается скидка и
отображается стоимость со скидкой.
* Затем добавляется налог штата, исходя из кода штата и цены
со скидкой и отображается итоговая стоимость с учетом
скидки и добавленного налога.

### Скидки

[таблица discounts](data/discounts.csv)

* amount - Стоимость заказа, USD
* rate - Скидка, %

| amount | rate |
| ------ | ---- |
| 1000   | 3    |
| 5000   | 5    |
| 7000   | 7    |
| 10000  | 10   |
| 50000  | 15   |

### Налоги

[таблица taxes](data/taxes.csv)

* state_name - Штат пользователя
* rate - Налоговая ставка, %

| state_name | rate |
| ---------- | ---- |
| UT         | 6.85 |
| NV         | 8    |
| TX         | 6.25 |
| AL         | 4    |
| CA         | 8.25 |

## Схема сервисов
![Services Schema](docs/schema.png)

## Инструкция для запуска

1. Для запуска сервиса выполнить команду `docker-compose up -d` и открыть в браузере http://localhost:18000
   
2. Для тестирования потребуется версия python >= 3.9
    * установка проекта и зависимостей `pip install .[test]`
    * линтер `flake8 .`
    * проверка статической типизации `mypy tom_calculator`
    * запуск тестов `pytest`
    
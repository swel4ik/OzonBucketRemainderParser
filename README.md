# Ozon Bucket Remainders Parser
Парсер количества остатков товаров в корзине для сайта https://www.ozon.ru/ 

Бот собирает информацию о товарах, находящихся в вашей корзине:
* Название товара
* Цвет
* Продавец
* Остаток на складе
## Установка
```
git clone https://github.com/swel4ik/OzonBucketRemainderParser.git
cd OzonBucketRemainderParser
pip install -r requirements.txt
```
## Подготовка к использованию
1. Открыть хром и залогиниться в свою учетную запись на https://www.ozon.ru/
2. Добавить интересующие товары к себе в корзину
3. Закрыть браузер
4. В `config.json` изменить значения в соответствии с вашим профилем в хроме
5. Запустить бота: `python ozonBot.py`


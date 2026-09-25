# antiskalant.uz — сайт ONSITE (антискаланты CLEAN RO)

Статический сайт на трёх языках (RU / UZ / EN), по дизайну и логике sdalimov.uz.

## Как собрать
```
python3 build.py
```
Готовый сайт появляется в папке `site/`. Её содержимое загружается в папку `domains/antiskalant.uz/public_html` на хостинге.

## Где править
- Все тексты на трёх языках: словарь `CONTENT` в `build.py`
- Контакты и домен: словарь `CONFIG` в `build.py`
- Стили: `site/style.css` (основа — sdalimov.uz, в конце блок «ONSITE additions»)

## Страницы
| RU | UZ | EN |
|---|---|---|
| / | /uz/ | /en/ |
| /antiscalant-clean-ro.html | /uz/antiskalant-clean-ro.html | /en/antiscalant-clean-ro.html |
| /industries.html | /uz/tarmoqlar.html | /en/industries.html |
| /dosing-service.html | /uz/dozalash-xizmati.html | /en/dosing-service.html |
| /projects-cases.html | /uz/loyihalar-keyslar.html | /en/projects-cases.html |
| /about.html | /uz/biz-haqimizda.html | /en/about.html |
| /news.html | /uz/yangiliklar.html | /en/news.html |

Также генерируются `sitemap.xml` (с hreflang), `robots.txt` и `llms.txt`. JSON-LD есть на всех страницах: Organization, Product, FAQPage, Service.

## Что нужно заполнить до запуска
1. Telegram компании (сейчас стоит t.me/sdalimov). Телефон, email и адрес взяты из TDS.
2. Картинка для соцсетей 1200×630 с логотипом (сейчас стоит фото)
3. PDF с TDS и SDS для скачивания (по желанию, после исправления опечаток в TDS)

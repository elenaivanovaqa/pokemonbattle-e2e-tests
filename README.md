### Запуск тестов
1. Переименовать .env_template в .env
2. При необходимости изменить переменные в .env на свои

Запустить тесты: pytest -v

Запустить тесты в headless-режиме (локально, с предподготовкой данных): pytest -v --prepare-data

Запуск c allure-отчётом (для справки): pytest -v --alluredir=allure-results

Запуск для снятия эталонных скриншотов (для справки): pytest -v tests/screenshot --update-snapshots



## Версия на main подготовлена к CI-запускам в headless-режиме:

1. В conftest.py добавлены запуски в headless при указании флага --prepare-data (фикстура driver), поддержка флага добавлена в pytest_addoption
2. Добавлена подготовка данных в фикстуре create_session_data и хелпер в helpers/prepare_session_data
3. Получение id тестового тренера и покемона в PageObject'ах и формирование зависящих от них локаторов сделано через получение переменных окружения при инициализации экземпляров класса (перенесено в __init__)
4. Добавлены настройки автоматического скипа тестов, которые не проходят в headless (напр. скриншотные) в pytest_configure и pytest_runtest_setup
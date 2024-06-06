## eng
### Description
This example provides a basic structure for organizing an API automation testing project. The goal is to promote a well-structured and maintainable approach to test development and execution.
### To run the tests:
1. Clone the repository.
2. Create and activate a virtual environment (venv):

      ```
      python3 -m venv venv

      # On Windows:
      venv\Scripts\activate

      # On macOS/Linux:
      source venv/bin/activate
      ```
3. Install dependencies: 

      `pip install -r requirements.txt`

4. Run the tests: 

      `pytest -rva tests/test_users.py`


## rus
### Описание
Этот пример демонстрирует базовую структуру организации проекта по автоматизированному тестированию API. Цель заключается в том, чтобы предложить хорошо организованный и поддерживаемый подход к разработке и выполнению тестов.
### Для запуска тестов необходимо:
1. Клонировать репозиторий
2. Создать и запустить venv:

      ```
      python3 -m venv venv

      # для Windows:
      venv\Scripts\activate

      # для macOS/Linux:
      source venv/bin/activate
      ```
3. Установить зависимости:
   
     `pip install -r requirements.txt`

4. Запустить тесты командой:

     `pytest -rva tests/test_users.py`

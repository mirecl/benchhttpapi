```bash
# Проверка сервиса Rust
curl -d '{"date":"31.12.2021","amount":10000,"rate":3.5,"periods":60}' -H "Content-Type: application/json" -X POST http://localhost:8080/deposit
# Проверка сервиса Golang
curl -d '{"date":"31.12.2021","amount":10000,"rate":3.5,"periods":60}' -H "Content-Type: application/json" -X POST http://localhost:8081/deposit
```

```bash
# Запуск сервиса locust (запуск нагрузки осуществляется через WEB-интерфейс http://127.0.0.1:8089)
./run.sh http://127.0.0.1:8080 nt.py 5
```
For check code use most popular linter:
+ flake8
```bash
pip install flake8
pip install flake8-bugbear
pip install flake8-eradicate
pip install flake8-fastapi # for only FastAPI
pip install flake8-functions-names 
pip install pep8-naming 
pip install flake8-docstrings
pip install flake8-pytest 
pip install flake8-annotations 
pip install flake8-black
pip install flake8-variables-names
```
+ pylint
```bash
pip install pylint
```
+ mypy
```bash
pip install mypy
```


```bash
# Запуск тестов
pytest -xs
```
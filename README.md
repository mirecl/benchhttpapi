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
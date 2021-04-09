```bash
# Проверка серивса на Rust
curl -d '{"date":"31.12.2021","amount":10000,"rate":3.5,"periods":60}' -H "Content-Type: application/json" -X POST http://localhost:8080/deposit
# Проверка серивса на Golang
curl -d '{"date":"31.12.2021","amount":10000,"rate":3.5,"periods":60}' -H "Content-Type: application/json" -X POST http://localhost:8081/deposit
```
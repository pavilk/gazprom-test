# Тестовые задания

- 01-python — задания 1-7 (Python, FastAPI)
- [02-jenkins](02-jenkins/README.md) — задание 8, Jenkins
- [task-9.md](task-9.md) — задание 9: приложение, systemd, docker, мониторинг, NAT, kubernetes
- [06-security](06-security/README.md) — задание 10, безопасность в kubernetes

Всё поднималось в Yandex Cloud. Приложение можно проверить так:

```
curl -X POST -H "Test: Hello" http://153.51.115.69:8000/
curl -X POST -H "Test: Hello" http://84.201.171.109/
```

Первый адрес - ВМ за NAT, второй - ingress в kubernetes.

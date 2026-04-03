# Payment Service Backend

Асинхронный REST API на Python (Sanic + SQLAlchemy + PostgreSQL)  
Проект для тестового задания: пользователи, администраторы, счета, платежи через вебхук.

---

## **Стек**

- Python 3.12  
- Sanic (асинхронный веб-фреймворк)  
- SQLAlchemy (ORM для работы с БД)  
- PostgreSQL  
- Docker + Docker Compose  

---

## **Тестовые данные**

| Роль        | Email               | Password   |
|------------|-------------------|------------|
| Пользователь | user@example.com   | userpass   |
| Администратор | admin@example.com | adminpass  |

---

## **Запуск через Docker Compose**

1. Постройте образы и запустите сервисы:

```bash
docker-compose build
docker-compose up

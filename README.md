# 🖥️ Веб-сервис для работы с комплектующими (Flask + Flasgger)

Этот проект представляет собой REST API для управления компьютерными комплектующими. Веб-сервис позволяет **добавлять, удалять, обновлять и фильтровать** комплектующие, а также получать статистику по ценам.

## 🚀 Функционал API
🔹 **Получение списка комплектующих** (с фильтрацией и сортировкой)  
🔹 **Добавление нового комплектующего**  
🔹 **Обновление информации о комплектующем**  
🔹 **Удаление комплектующего**  
🔹 **Вычисление средней, максимальной и минимальной цены**  

Документация API автоматически генерируется с помощью **Swagger (Flasgger)**.

---

## 🛠️ Установка и запуск

### **1️⃣ Установка зависимостей** 
```bash
git clone https://github.com/ТВОЙ_ЛОГИН/lab2-web-service.git
cd lab2-web-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
### **2️⃣ Запуск сервера**
```bash
python main.py
```
### 3️⃣ Открыть Swagger UI
После запуска открой в браузере:
http://127.0.0.1:5000/apidocs/

## Автор
#### Мурзыков Андрей Валерьевич - Студент ФДО ТУСУР, группа з-434П8-4
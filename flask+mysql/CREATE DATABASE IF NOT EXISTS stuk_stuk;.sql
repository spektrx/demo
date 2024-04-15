CREATE DATABASE IF NOT EXISTS stuk_stuk; -- Создание базы данных, если ее нет

USE stuk_stuk; -- Использование созданной базы данных

-- Создание таблицы для пользователей
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL
);

-- Создание таблицы для заявок
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    username VARCHAR(255) NOT NULL,
    status ENUM('New', 'Done', 'Reject') NOT NULL DEFAULT 'New',
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

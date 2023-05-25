-- Создание базы данных hh_ru и таблиц в ней: employers, vacancies.

-- DROP DATABASE IF EXISTS hh_ru;
-- CREATE DATABASE hh_ru;

DROP TABLE IF EXISTS employers;
DROP TABLE IF EXISTS vacancies;

CREATE TABLE employers
(
    employer_id varchar(10),
    employer_name varchar(255) NOT NULL ,
    employer_industry varchar(255),
    employer_city varchar(255),
    employer_url varchar(255),
    employer_open_vacancies int,

    CONSTRAINT pk_employers_employer_id PRIMARY KEY (employer_id)
);

CREATE TABLE vacancies
(
    vacancy_id varchar(10),
    vacancy_name varchar(255) NOT NULL ,
    vacancy_city varchar(255),
    vacancy_url varchar(255),
    vacancy_salary decimal,
    published_at date,
    employer_id varchar(10),

    CONSTRAINT pk_vacancies_vacancy_id PRIMARY KEY (vacancy_id),
    CONSTRAINT fk_vacancies_employer_id FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
);



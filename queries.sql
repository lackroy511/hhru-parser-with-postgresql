-- `get_companies_and_vacancies_count()`: получает список всех компаний и количество вакансий у каждой компании.
select employer_name, count(*) as open_vacancies
from employers
inner join vacancies using(employer_id)
group by employer_name;

-- `get_all_vacancies()`: получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
select employer_name, vacancy_name, vacancy_salary, vacancy_url
from employers
inner join vacancies using(employer_id);

-- `get_avg_salary()`: получает среднюю зарплату по вакансиям.
select avg(vacancy_salary) as avg_salary
from vacancies;

-- `get_vacancies_with_higher_salary()`: получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
select * from vacancies
where vacancy_salary > (select avg(vacancy_salary)
from vacancies);

-- `get_vacancies_with_keyword()`: получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
select *
from vacancies
where vacancy_name
LIKE '%Python%' or vacancy_name LIKE '%python%';

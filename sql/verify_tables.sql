SELECT name 
FROM sqlite_master 
WHERE type = 'table';

select * from boston_employee LIMIT 10;

SELECT * FROM budgets LIMIT 10;

SELECT * 
FROM newest_invoices_data
order by id_invoice ASC;

SELECT *
From boston_employee
WHERE total_gross < 0;




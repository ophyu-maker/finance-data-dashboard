CREATE VIEW IF NOT EXISTS department_annual_actual AS
SELECT
    department_name,
    SUM(
        COALESCE(regular, 0)
      + COALESCE(retro, 0)
      + COALESCE(other, 0)
      + COALESCE(overtime, 0)
      + COALESCE(injured, 0)
      + COALESCE(detail, 0)
      + COALESCE(quinn_education, 0)
    ) AS annual_actual_pay
FROM boston_employee
GROUP BY department_name;

SELECT * FROM department_annual_actual LIMIT 10;

DROP VIEW IF EXISTS department_monthly_actual;

CREATE VIEW IF NOT EXISTS department_monthly_actual AS
SELECT
    department_name,
    round(annual_actual_pay / 12.0, 2) AS monthly_actual_pay
FROM department_annual_actual;

select * from department_monthly_actual limit 10;

SELECT
    b.month,
    b.department_name,
    b.budget_category,
    b.budget_amount,
    a.monthly_actual_pay,
    a.monthly_actual_pay - b.budget_amount AS variance,
    ROUND(
        ((a.monthly_actual_pay - b.budget_amount) / b.budget_amount) * 100,
        2
    ) AS variance_pct
FROM budgets b
LEFT JOIN department_monthly_actual a
    ON b.department_name = a.department_name
ORDER BY b.month, b.department_name;

CREATE VIEW IF NOT EXISTS department_annual_budget AS
	SELECT department_name, 
	sum(budget_amount) as budget_annual_amount
	FROM budgets 
	GROUP BY department_name;

SELECT * FROM department_annual_budget;

SELECT b.department_name, b.budget_annual_amount,
			 a.annual_actual_pay, a.annual_actual_pay - b.budget_annual_amount AS variance,
			 ROUND(
				((a.annual_actual_pay - b.budget_annual_amount)/ b.budget_annual_amount) * 100 , 2) AS variance_pct
			FROM deparment_annual_budget b
			LEFT JOIN department_annual_actual a
			ON b.department_name = a.department_name;
			
SELECT title, sum(overtime) as overtime
FROM boston_employee
GROUP BY title
ORDER BY overtime DESC;

SELECT department_name, title,  sum(injured) as injured_compensation
FROM boston_employee
WHERE injured > 0
GROUP BY title
ORDER BY injured_compensation DESC;
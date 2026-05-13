DROP VIEW IF EXISTS invoice_cleaned;

CREATE VIEW invoice_cleaned AS
SELECT
    id_invoice,
	client,
    issuedDate AS issued_date,
    strftime('%Y-%m', issuedDate) AS invoice_month,
	dueDate AS due_date,
	strftime('%Y-%m', dueDate) AS due_month,
    country,
    service,
    total,
    discount,
    tax,
    invoiceStatus as invoice_status,
    balance,
    ROUND(total - discount + tax, 2) AS net_invoice_amount
FROM newest_invoices_data;

SELECT * FROM invoice_cleaned LIMIT 10;

DROP VIEW IF EXISTS monthly_invoice_summary;

CREATE VIEW monthly_invoice_summary AS
SELECT
    invoice_month,
    COUNT(*) AS invoice_count,
    ROUND(SUM(total), 2) AS total_invoiced,
    ROUND(SUM(discount), 2) AS total_discount,
    ROUND(SUM(tax), 2) AS total_tax,
    ROUND(SUM(balance), 2) AS total_outstanding_balance,
    ROUND(SUM(net_invoice_amount), 2) AS total_net_invoice_amount
FROM invoice_cleaned
GROUP BY invoice_month
ORDER BY invoice_month;

SELECT * FROM monthly_invoice_summary LIMIT 10;

DROP VIEW IF EXISTS invoice_status_summary;

CREATE VIEW invoice_status_summary AS
SELECT
    invoice_status,
    COUNT(*) AS invoice_count,
    ROUND(SUM(total), 2) AS total_invoice_amount,
    ROUND(SUM(balance), 2) AS outstanding_balance
FROM invoice_cleaned
GROUP BY invoice_status
ORDER BY outstanding_balance DESC;

SELECT * FROM invoice_status_summary;

DROP VIEW IF EXISTS company_status_summary;

CREATE VIEW company_status_summary AS
SELECT
	client,
    invoice_status,
    COUNT(*) AS invoice_count,
    ROUND(SUM(total), 2) AS total_invoice_amount,
    ROUND(SUM(balance), 2) AS outstanding_balance,
	ROUND(SUM(SUM(balance)) OVER (PARTITION BY client
						ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS vendor_total_outstanding_balance
FROM invoice_cleaned
WHERE invoice_status != "Paid"
GROUP BY client, invoice_status
ORDER BY client, vendor_total_outstanding_balance;

select * from company_status_summary limit 20;

DROP VIEW IF EXISTS invoice_service_summary;

CREATE VIEW invoice_service_summary AS
SELECT
    service,
    COUNT(*) AS invoice_count,
    ROUND(SUM(total), 2) AS total_invoiced,
    ROUND(SUM(balance), 2) AS outstanding_balance,
    ROUND(AVG(total), 2) AS avg_invoice_amount
FROM invoice_cleaned
GROUP BY service
ORDER BY total_invoiced DESC;

SELECT *
FROM invoice_service_summary;

DROP VIEW IF EXISTS invoice_country_summary;

CREATE VIEW invoice_country_summary AS
SELECT
    country,
    COUNT(*) AS invoice_count,
    ROUND(SUM(total), 2) AS total_invoiced,
    ROUND(SUM(balance), 2) AS outstanding_balance
FROM invoice_cleaned
GROUP BY country
ORDER BY outstanding_balance DESC;

SELECT *
FROM invoice_country_summary;
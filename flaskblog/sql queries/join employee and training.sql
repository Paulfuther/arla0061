-- SQLite
select firstname, lastname, whmis.compliant
from employee
inner join whmis  on employee_id = Employee.id

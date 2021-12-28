-- SQLite
select  employee.firstname, employee.id, store.number, 
User.active, staffschedule.shift_description, staffschedule.shift_date
from employee

inner join User on employee.user_id = User.id
left outer join staffschedule on employee.id = staffschedule.employee_id
inner join store on employee.store_id = Store.id


where employee.store_id = 3 and user.active = 1
order by firstname


-- SQLite
select firstname, lastname, course_id, name
from employee
inner join course_users  on employee_id = employee.id
inner join course on course_id = course.id
order by firstname

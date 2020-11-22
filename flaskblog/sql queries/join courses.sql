select firstname, lastname, course.name, value

from employee
    inner join grade on employee_id = employee.id
    inner join course on course_id = course.id
    

order by firstname
select firstname, course.name, completedcourse.score

from employee
    inner join course_employee on employee_id = employee.id
    inner join course on course.id = course_id
    inner join course_complete on course_id = course_employee.id

order by firstname
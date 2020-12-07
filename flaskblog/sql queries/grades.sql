select firstname, lastname, Course.id, Course.name, value


from grade


inner join employee on employee.id = employee_id
inner join Course on course.id = course_id

where value
= "n"
order by firstname
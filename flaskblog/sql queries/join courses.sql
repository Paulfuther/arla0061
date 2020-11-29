select firstname, lastname, hrfiles.text

from employee
    inner join hrfiles on employee_id = employee.id
    
    

order by firstname
select firstname, lastname, hrfiles.text

from employee
    inner join Empfile on employee2_id = employee.id
    inner join hrfiles on hrfiles.id = file_id
    
    

order by firstname
select firstname, lastname, shift_description, number, active

from employee, store, user

    
    inner join staffschedule on employee_id = employee.id
    inner join user on user.id = employee.user_id
    
    
    where store.number = 33485 
    
    
    
    

order by employee.id
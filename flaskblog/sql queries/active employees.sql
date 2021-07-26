-- SQLite
select  employee.firstname, store.number, employee.email, User.active from employee
inner join User on employee.user_id = User.id
inner join store on employee.store_id = Store.id
where User.active = 1
order by number


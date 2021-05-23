-- SQLite
select  employee.firstname, Store.number from employee
inner join store on employee.store_id = Store.id
where employee.id not in (select employee2_id from Empfile)
order by store_id


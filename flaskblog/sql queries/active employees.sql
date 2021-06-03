-- SQLite
select  employee.firstname, User.active from employee
inner join User on employee.user_id = User.id
where User.active = 1
order by firstname


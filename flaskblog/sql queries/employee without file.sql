-- SQLite
select * from employee
where id not in (select employee2_id from Empfile)
order by store


-- SQLite
select firstname, lastname, role.name
from user
inner join role  on role.id = user.id

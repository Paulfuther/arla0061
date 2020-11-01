-- SQLite
select firstname, role.name

from user
inner join roles_users  on user_id = user.id
inner join role on role.id = role_id

order by firstname



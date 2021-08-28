select user.user_name, user.id, role_id from user
inner join roles_users on user.id = roles_users.user_id
where role_id=3
order by user.user_name


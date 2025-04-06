with company_avg as (
  select avg(salary) as comp_avg
  from employees
)

SELECT
  d.id as department_id,
  coalesce(avg(e.salary),0) as department_avg_salary,
  CASE
    when coalesce(avg(e.salary),0) > c.comp_avg then 'Above'
    when coalesce(avg(e.salary),0) < c.comp_avg then 'Below'
    else 'Equal'
  end as status
from departments d
left join employees e
  on e.departmentId = d.id
cross join company_avg c
group by 
  d.id,
  c.comp_avg
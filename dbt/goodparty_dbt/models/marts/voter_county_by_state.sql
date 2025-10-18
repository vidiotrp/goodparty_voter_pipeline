with base as (
    select *
    from {{ ref('int_voters_cleaned') }}
),

last_year as (
    select 
        *,
        case 
            when last_voted_date is null or last_voted_date < current_date - interval '1 year'
            then 1 
            else 0 
        end as not_voted_last_year
    from base
),

final as (
select
    state,
    count(*) as total_voters,
    count(case when gender = 'M' then 1 end) as male_voters,
    count(case when gender = 'F' then 1 end) as female_voters,
    avg(age) as avg_age,
    max(age) as max_age,
    min(age) as min_age,
    sum(case when email is null or email = '' then 1 else 0 end) as voters_without_email,
    sum(not_voted_last_year) as voters_not_voted_last_year
from last_year
group by state
order by total_voters desc
)

select * from final
with raw as (
    select *
    from {{ source('voter_staging', 'voter_staging') }}
),

cleaned as (
select
    voter_id,
    first_name,
    last_name,
    age,
    gender,
    state,
    party,
    email,
    registered_date,
    last_voted_date,
    current_date
from raw
)

select * from cleaned
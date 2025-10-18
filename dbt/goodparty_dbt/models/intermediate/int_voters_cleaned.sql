with raw as (
    select *
    from {{ ref('stg_voters') }}
),

state_map as (
    select *
    from {{ ref('state_mappings') }}  
),

voters_cleaned as (
    select
        v.voter_id,
        initcap(v.first_name) as first_name,
        initcap(v.last_name) as last_name,
        initcap(v.last_name || ', ' || v.first_name) as full_name,
        v.age,
        upper(v.gender) as gender,
        coalesce(sm.abbreviation, upper(v.state)) as state,
        upper(v.party) as party,
        lower(v.email) as email,
        v.registered_date::date as registered_date,
        v.last_voted_date::date as last_voted_date,
        current_date as updated_at,
        case when v.email is null or v.email = '' then true else false end as missing_email,
        case when v.age is null then true else false end as missing_age,
        case when v.state is null or v.state = '' then true else false end as missing_state,
        case when v.party is null or v.party = '' then true else false end as missing_party,
        case when v.first_name is null or v.first_name = '' then true else false end as missing_first_name,
        case when v.last_name is null or v.last_name = '' then true else false end as missing_last_name
    from raw v
    left join state_map sm
        on upper(v.state) = upper(sm.full_name)
)

select * from voters_cleaned

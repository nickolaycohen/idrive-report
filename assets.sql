--  assets
-- All account
select sum(size), 
    case 
--        when sum(p.size) / 1000000000000 > 0
--        then cast(sum(p.size) / 1000000000000 as text) || ' TB'
        when sum(p.size) / 1000000000 > 0
        then cast(sum(p.size) / 1000000000 as text) || ' GB'
        when sum(p.size) / 1000000 > 0
        then cast(sum(p.size) / 1000000 as text) || ' MB'
        when sum(p.size) / 1000 > 0
        then cast(sum(p.size) / 1000 as text) || ' kB'
        else cast(sum(p.size) as text) || ' B'
    end as sizeB
from paths p
inner join devices d on d.device_id = p.device_id 
where parent_path = '//'
order by 1 desc

-- largest devices 
select sum(size), 
    case 
--        when sum(p.size) / 1000000000000 > 0
--        then cast(sum(p.size) / 1000000000000 as text) || ' TB'
        when sum(p.size) / 1000000000 > 0
        then cast(sum(p.size) / 1000000000 as text) || ' GB'
        when sum(p.size) / 1000000 > 0
        then cast(sum(p.size) / 1000000 as text) || ' MB'
        when sum(p.size) / 1000 > 0
        then cast(sum(p.size) / 1000 as text) || ' kB'
        else cast(sum(p.size) as text) || ' B'
    end as sizeB, 
p.device_id, d.nick_name
from paths p
inner join devices d on d.device_id = p.device_id 
where parent_path = '//'
group by p.device_id, d.nick_name
order by 1 desc

-- all not-drilled down and untagged paths by size
SELECT        case 
        when p.size / 1000000000000 > 0
        then cast(p.size / 1000000000000 as varchar) || ' TB'
        when p.size / 1000000000 > 0
        then cast(p.size / 1000000000 as varchar) || ' GB'
        when p.size / 1000000 > 0
        then cast(p.size / 1000000 as varchar) || ' MB'
        when p.size / 1000 > 0
        then cast(p.size / 1000 as varchar) || ' kB'
        else cast(p.size as varchar) || ' B'
    end as sizeB, d.nick_name, p.name, p.parent_path
from paths p
join devices d on d.device_id = p.device_id
where p.drilled_down = FALSE and p.tag = ''
order by p.size desc

-- all tagged paths by size
SELECT        case 
        when p.size / 1000000000000 > 0
        then cast(p.size / 1000000000000 as varchar) || ' TB'
        when p.size / 1000000000 > 0
        then cast(p.size / 1000000000 as varchar) || ' GB'
        when p.size / 1000000 > 0
        then cast(p.size / 1000000 as varchar) || ' MB'
        when p.size / 1000 > 0
        then cast(p.size / 1000 as varchar) || ' kB'
        else cast(p.size as varchar) || ' B'
    end as sizeB, d.nick_name, p.name, p.parent_path, p.drilled_down, p.tag
from paths p
join devices d on d.device_id = p.device_id
-- where p.tag <> ''
order by p.size desc, d.nick_name, p.parent_path, p."name"

-- reset DB
delete 
from paths;

delete 
from devices;
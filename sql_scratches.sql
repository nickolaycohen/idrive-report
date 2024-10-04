-- untagged and notDrilled Down
select p.deviceId, d.nickName, p.parentPath, p.name, p.size, 
    case 
        when p.size / 1000000000000 > 0
        then cast(p.size / 1000000000000 as string) || ' TB'
        when p.size / 1000000000 > 0
        then cast(p.size / 1000000000 as string) || ' GB'
        when p.size / 1000000 > 0
        then cast(p.size / 1000000 as string) || ' MB'
        when p.size / 1000 > 0
        then cast(p.size / 1000 as string) || ' kB'
        else cast(p.size as string) || ' B'
    end as sizeB, 
p.fileCount, p.tag
from paths p
join devices d on d.deviceId = p.deviceId
where p.drilledDown = 0 and p.tag = ''
order by p.size desc

-- tagged
select p.deviceId, d.nickName, p.parentPath, p.name, p.size,     
    case 
        when p.size / 1000000000000 > 0
        then cast(p.size / 1000000000000 as string) || ' TB'
        when p.size / 1000000000 > 0
        then cast(p.size / 1000000000 as string) || ' GB'
        when p.size / 1000000 > 0
        then cast(p.size / 1000000 as string) || ' MB'
        when p.size / 1000 > 0
        then cast(p.size / 1000 as string) || ' kB'
        else cast(p.size as string) || ' B'
    end as sizeB, 
p.fileCount, p.tag
from paths p
join devices d on d.deviceId = p.deviceId
where p.tag <> ''
order by p.size desc

select * 
from paths
where deviceId = 'R01563807439000950037'

SELECT tag as 'tag' from paths where deviceId=:device_id and name=:name and parentPath=:parentPath

select p.deviceId, d.nickName, p.parentPath, p.name, p.size, p.fileCount, p.drilledDown, p.tag
from paths p
join devices d on d.deviceId = p.deviceId
order by p.size desc

-- largest devices 
select sum(size), 
    case 
        when sum(p.size) / 1000000000000 > 0
        then cast(sum(p.size) / 1000000000000 as string) || ' TB'
        when sum(p.size) / 1000000000 > 0
        then cast(sum(p.size) / 1000000000 as string) || ' GB'
        when sum(p.size) / 1000000 > 0
        then cast(sum(p.size) / 1000000 as string) || ' MB'
        when sum(p.size) / 1000 > 0
        then cast(sum(p.size) / 1000 as string) || ' kB'
        else cast(sum(p.size) as string) || ' B'
    end as sizeB, 
p.deviceId, d.nickName
from paths p
inner join devices d on d.deviceId = p.deviceId
where parentPath = '//'
group by p.deviceId
order by 1 desc

-- NickolaysiMac not drilled down
select 
    case 
        when p.size / 1000000000000 > 0
        then cast(p.size / 1000000000000 as string) || ' TB'
        when p.size / 1000000000 > 0
        then cast(p.size / 1000000000 as string) || ' GB'
        when p.size / 1000000 > 0
        then cast(p.size / 1000000 as string) || ' MB'
        when p.size / 1000 > 0
        then cast(p.size / 1000 as string) || ' kB'
        else cast(p.size as string) || ' B'
    end as sizeB, 
d.nickName, p.parentPath, p.name, p.drilledDown
from paths p
inner join devices d on d.deviceId = p.deviceId
where p.deviceId = 'D01563744743000489825' and drilledDown = 0 
order by p.size desc

-- NickolaysiMac/Users/nickolaycohen
select 
    case 
        when p.size / 1000000000000 > 0
        then cast(p.size / 1000000000000 as string) || ' TB'
        when p.size / 1000000000 > 0
        then cast(p.size / 1000000000 as string) || ' GB'
        when p.size / 1000000 > 0
        then cast(p.size / 1000000 as string) || ' MB'
        when p.size / 1000 > 0
        then cast(p.size / 1000 as string) || ' kB'
        else cast(p.size as string) || ' B'
    end as sizeB, 
p.deviceId, d.nickName, p.parentPath, p.name
from paths p
inner join devices d on d.deviceId = p.deviceId
where parentPath = '//Users/nickolaycohen' and p.deviceId = 'D01563744743000489825'
order by p.size desc



select 
    case 
        when p.size / 1000000000000 > 0
        then cast(p.size / 1000000000000 as string) || ' TB'
        when p.size / 1000000000 > 0
        then cast(p.size / 1000000000 as string) || ' GB'
        when p.size / 1000000 > 0
        then cast(p.size / 1000000 as string) || ' MB'
        when p.size / 1000 > 0
        then cast(p.size / 1000 as string) || ' kB'
        else cast(p.size as string) || ' B'
    end as sizeB, 
p.deviceId, d.nickName, p.parentPath, p.name, p.size, p.fileCount
from paths p
inner join devices d on d.deviceId = p.deviceId
where p.deviceId = 'D01563744743000489825'
order by p.size desc
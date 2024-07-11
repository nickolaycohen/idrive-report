--8/21 2023
select count(*) 
from zasset
-- 68841

select *
from zasset
limit 1

-- all files by size
select aa.zoriginalfilesize, aa.zasset, aa.zoriginalfilename
from zadditionalassetattributes aa
order by aa.zoriginalfilesize desc
limit 50

-- asset by zwellchosensubjectscore
select zc.zwellchosensubjectscore, zc.zasset, aa.zoriginalfilename
from zcomputedassetattributes zc
join zadditionalassetattributes aa on aa.zasset = zc.zasset
order by 1 desc
limit 20

-- asset by zinteractionscore
select zc.zinteractionscore, zc.zasset, aa.zoriginalfilename
from zcomputedassetattributes zc
join zadditionalassetattributes aa on aa.zasset = zc.zasset
order by 1 desc
limit 20

-- original and db name
select aa.zoriginalfilename, a.zdirectory, a.zfilename, a.zuuid
from zadditionalassetattributes aa
join zasset a on a.z_pk = aa.zasset
where aa.zoriginalfilename = 'NMS_9788.MOV'
order by 1 desc
limit 20

select aa.zoriginalfilename
from zadditionalassetattributes aa
where aa.zoriginalfilename = 'NMS_9788.MOV'

select aa.zoriginalfilename, aa.zasset, aa.ztitle, aa.zimportsessionid
from zadditionalassetattributes aa
limit 1

select aa.zimportsessionid, count(*)
from zadditionalassetattributes aa
group by aa.zimportsessionid
order by 2 desc

select *
from zasset
where z_pk = 4


select zdirectory, zfilename, zuuid, zkind, * 
from zasset
where z_pk = 68468

select *
from zalbumlist

select ztitle, zuuid, zkeyasset, *
from zgenericalbum
order by ztitle 

select zdirectory, zfilename, zuuid, zkind, * 
from zasset
where z_pk = 12311

-- how many assets
select count(*)
from zasset

-- get one asset
select *
from zasset
limit 5

-- imports count by session
select zimportsession, count(*)
from zasset
group by zimportsession
order by 2 desc

select max(zimportsession)
from zasset

-- 
select z_26albums, count(*)
from z_26assets
group by z_26albums

-- possibly root albums
select *
from zalbumlist
where z_pk = 50

--
select *
from z_25albumlists

514	26988
442	25174
429	3231

select zimportsessionid
from zadditionalassetattributes
limit 1
where zimportsessionid = 514

-- find import session counts
select zimportsession, count(*)
from zasset
group by zimportsession
order by 2 desc
limit 10

select * 
from zcloudmaster

where zimportsessionid= 514

select count(*)
from zasset

select *
from zgenericalbum
where ztitle = 2023

select count(*)
from z_26assets
where z_26albums = 254 --254 

select * 
from z_26assets
limit 5

-- albums
select ga.z_pk, ga.zuuid, ga.ztitle, ga.zparentfolder, p.ztitle, ga.zcachedcount, ga.zkeyasset
from zgenericalbum ga
join zgenericalbum p on p.z_pk = ga.zparentfolder
order by p.ztitle, p.z_pk, ga.ztitle

select *
from zasset
where z_pk = 36331

select aa.zoriginalfilename, aa.zasset, aa.ztitle, aa.zimportsessionid
from zadditionalassetattributes aa
limit 1

-- album key asset
select aa.zoriginalfilename, a.zdirectory, a.zfilename, a.zuuid
from zadditionalassetattributes aa
join zasset a on a.z_pk = aa.zasset
where a.z_pk = 36331 --'NMS_9788.MOV'
order by 1 desc

-- assets in Album Eva
select *
from z_28assets
where z_28albums = 492

-- find 
136 2007

select *
from z_28assets
where z_28albums = 136


select *
from zcomputedassetattributes
order by 


-- all assets
select count(*) 
from zasset

-- order assets by overallscore
select a.z_pk, a.zuuid, a.ZOVERALLAESTHETICSCORE, aaa.zoriginalfilesize, aaa.zoriginalfilename, 
coalesce(cast(strftime('%s',replace(substr(aaa.zexiftimestampstring,-19,10),':','-') || ' ' || substr(aaa.zexiftimestampstring,-8,8)) as int), 
(a.zdatecreated + 978317999.796)) as epochTime,
datetime(coalesce(cast(strftime('%s',replace(substr(aaa.zexiftimestampstring,-19,10),':','-') || ' ' || substr(aaa.zexiftimestampstring,-8,8)) as int), 
(a.zdatecreated + 978317999.796)), 'unixepoch', 'localtime') as dateCreated
/*, julianday(a.zmodificationdate) , a.zmodificationdate,a.*, aaa.* */
from zasset a
join zadditionalassetattributes aaa on aaa.zasset = a.z_pk
where aaa.zoriginalfilename in ('IMG_0264.JPG', 'IMG_3977.HEIC')
order by a.ZOVERALLAESTHETICSCORE desc


-- find deamon updates
select *
from zmoment
order by zcontentscore desc
-- 0.76832361203705	0	707CFB58-5F60-4856-8F1D-D5B12C07423A

-- v6
select a.z_pk, a.zuuid, a.ZOVERALLAESTHETICSCORE, aaa.zoriginalfilesize, aaa.zoriginalfilename,
coalesce(cast(strftime('%s',replace(substr(aaa.zexiftimestampstring,-19,10),':','-') || ' ' || substr(aaa.zexiftimestampstring,-8,8)) as int), 
(a.zdatecreated + 978317999.796)) as epochTime
from zasset a
join zadditionalassetattributes aaa on aaa.zasset = a.z_pk
order by a.ZOVERALLAESTHETICSCORE desc

-- order assets by overallscore
select a.z_pk, a.zuuid, a.ZOVERALLAESTHETICSCORE, aaa.zoriginalfilesize, aaa.zoriginalfilename, 
coalesce(cast(strftime('%s',replace(substr(aaa.zexiftimestampstring,-19,10),':','-') || ' ' || substr(aaa.zexiftimestampstring,-8,8)) as int), 
(a.zdatecreated + 978317999.796)) as epochTime,
datetime(coalesce(cast(strftime('%s',replace(substr(aaa.zexiftimestampstring,-19,10),':','-') || ' ' || substr(aaa.zexiftimestampstring,-8,8)) as int), 
(a.zdatecreated + 978317999.796)), 'unixepoch', 'localtime') as dateCreated
/*, julianday(a.zmodificationdate) , a.zmodificationdate,a.*, aaa.* */
from zasset a
join zadditionalassetattributes aaa on aaa.zasset = a.z_pk
/*where aaa.zoriginalfilename in ('IMG_0264.JPG', 'IMG_3977.HEIC')*/
order by coalesce(cast(strftime('%s',replace(substr(aaa.zexiftimestampstring,-19,10),':','-') || ' ' || substr(aaa.zexiftimestampstring,-8,8)) as int), 
(a.zdatecreated + 978317999.796))


select * from assets.devices
select * from assets.paths


SELECT datetime(replace(lmd, '/', '-')) as 'lmd' from assets.paths 

select d.nickName, p.* 
from assets.paths p
left join devices d on d.deviceId = p.deviceId
order by p.size desc

SELECT parentPath as 'parentPath' from paths where deviceId=:device_id and name=:name

select last_insert_rowid()



select replace(parentPath || '/' || name,'///','//'), * from paths
order by size desc

select * from paths
where deviceId = 'D01692572940000295373' and drilledDown = 0
order by deviceId, parentPath, name

SELECT drilledDown as 'drilledDown' 
from paths 
where deviceId=:device_id and parentPath || name=:path

SELECT drilledDown as 'drilledDown' 
from paths 
where deviceId=:device_id and parentPath || '/' || name=:name

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

select *
from paths p

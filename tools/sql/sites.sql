select * from sites;
insert into sites (siteid, sitename, vendorefficient, panelnumber, panelsurface, panelref, latitude, longitude)
select 1723771, 'MSS:Deviation', 0.1908, 112, 1.635, 'DualSun Spring 315 black',43.3682871, 5.30575;

update sites
set kwhPrice = 0.1567
where siteid=2168697;

alter table sites
add column kwhPrice numeric;

update sites
set kwhPrice = 0.1207
where siteid=1723771;

select kwhprice from sites where siteid=1723771;


SELECT
ROUND((sum((data->'value')::numeric) * (select kwhprice from sites where siteid=1723771) / 1000), 1) as "Deviation Daily Cash"
FROM iowatt
WHERE
  label = 'energy'
  and siteid = 1723771
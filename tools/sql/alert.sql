
--deviation 1723771
--boris 2168697

select datatime , data->>'inverterMode' as inverterMode from iowatt
where
siteid = 2168697
and label = 'equipment_inverter'
and data->>'inverterMode' not in ('MPPT', 'SLEEPING')
order by datatime;


select datatime , data->'groundFaultResistance', data as groundFaultResistance from iowatt
where
siteid = 1723771
and label = 'equipment_inverter'
order by datatime DESC;
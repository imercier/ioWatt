select
DATE_TRUNC('day',timestamp) AS currentday,
sum(energyProduced) as "Total Produced engery W.h"
FROM EnergyHistory
where DATE_TRUNC('day',timestamp) >= '2021-06-21'
GROUP BY currentday
order by currentday desc;

select 
DATE_TRUNC('day',timestamp) AS currentday,
round(0.1972 * 21 * 1.66 * sum(radiation) * 0.5) as "Theorical Total Energy (W.h)"
from radiation
where DATE_TRUNC('day',timestamp) >= '2021-06-21'
GROUP BY currentday
order by currentday desc;

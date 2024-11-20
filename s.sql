-- SQLite
SELECT branch_market.market_type,
branch_market.name,branch_city.name,
branch_city.id,branch_province.name
 from branch_market JOIN branch_city on
  branch_market.city_id = branch_city.id 
  JOIN branch_province on 
  branch_province.id = branch_city.province_id
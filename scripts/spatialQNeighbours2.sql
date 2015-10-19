-- Sorted k-nearest neighbours 
SELECT UUID
  FROM ax31001
  WHERE ST_Isvalid(wkb_geometry)
  AND ST_Within(wkb_geometry,(
    SELECT ST_Buffer(
      ST_Centroid((
        SELECT wkb_geometry
        FROM ax31001
        WHERE uuid = 'DEHHALKA10000wlY')), 500)))
    AND uuid != 'DEHHALKA10000wlY'
  ORDER BY wkb_geometry <-> (
    SELECT wkb_geometry
    FROM ax31001
    WHERE uuid = 'DEHHALKA10000wlY')
  LIMIT 30;
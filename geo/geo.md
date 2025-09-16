# Create 3-scale nested square grid: Switzerland, Europe, World
CRS: [epsg:4326 (WGS84)](https://epsg.io/4326)
Each scale is nested within the next one (borders coincide)  
Center point: 47.0 N, 7.5 E (Bern, Switzerland)  
Initial zoom bounding box: 41.0 N, 53.0 N, 0.0 E, 15.0 E.  
Max zoomed out bounding box: -55 N, 70N, -130 E, 180 E.  
## Switzerland
Bounds: 45.0 N, 49.0 N, 5.0 E, 10.0 E.  
Spacing: 0.2dd N (vertical), 0.25dd E (horizontal)  
Num cells: 20 vertical X 20 horizontal = 400 cells  
## Europe
Bounds: 37.0 N, 57.0 N, -6.25 E, 18.75 E.  
Spacing: 1dd N (vertical), 1.25dd E (horizontal)  
Num cells: 20 vertical X 20 horizontal = 400 cells  
## World
Bounds: -53.0 N, 67.0 N, -125.0 E, 175.0 E.  
Spacing: 1dd N (vertical), 1.25dd E (horizontal)  
Num cells: 24 vertical X 48 horizontal = 1152 cells  
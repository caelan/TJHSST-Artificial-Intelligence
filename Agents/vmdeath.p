set dgrid3d 200, 100
set style data lines
set xlabel "metabolism"
set ylabel "vision"
set zlabel "deaths"
splot "vmdeath.txt"
pause -1

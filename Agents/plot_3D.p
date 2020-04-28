set terminal png
set output "vmdeath.png"
set dgrid3d 200, 100
set style data lines
set xlabel "metabolism"
set ylabel "vision"
set zlabel "deaths"
splot "vmdeath.txt"

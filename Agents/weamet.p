set terminal png
set output "weamet.png"
set title "t=100 steps"
set xlabel "metabolism"
set ylabel "wealth"
set xrange [0:5]
plot "weamet.txt" with boxes notitle

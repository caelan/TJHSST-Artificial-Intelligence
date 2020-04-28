set terminal png
set output "visdis.png"
set title "t=100 steps"
set xlabel "vision"
set ylabel "avg distance from place-of-birth"
set xrange [0:500]
plot "visdis.txt" with boxes notitle

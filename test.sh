declare -a problems=("knapsack")
declare -A epochs=(["SA"]=10 ["TABU"]=1)

for PROBLEM in ${problems[@]}; do
    for METHOD in ${!epochs[@]}; do
        OUTPUT=$PROBLEM/result/$PROBLEM\_$METHOD.csv
        ITER=${epochs[$METHOD]}

        printf "file,otimal,%s,\n" $(seq -s ',' $ITER) > $OUTPUT
        for FILE in $PROBLEM/input/*; do
            read ans < $PROBLEM/output/$(basename $FILE)
            LC_NUMERIC="C" printf "%s,%.2f," $(basename $FILE) $ans
            for i in $(seq $ITER); do
                result=$(pypy3 $PROBLEM/main.py $METHOD < $FILE)
                LC_NUMERIC="C" printf "%.2f," $result
            done
            printf "\n"
        done >> $OUTPUT
    done 
done
 #!/bin/bash

file=$1
file2=$2
awk  -F '\t' 'BEGIN{
    OFS="\t"
}ARGIND==1{
    d[$9] = 1    
}ARGIND==2{
    #split($1,a,"#")
    #if(d[a[2]]==1){
    if(d[$1]==1){

    print $0 
    }
}' ${file} ${file2}



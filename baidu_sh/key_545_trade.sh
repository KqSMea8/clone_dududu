#!/bin/sh
# sunfuhao

file=$1;
dd=$2;
week=$3;
#好看总体
awk -F"\t" -v dd=$dd -v week=$week 'BEGIN{
    OFS = "\t";
}
{
    split($1,a,"#")
    if(a[1]!="545" && a[1]!="628" && a[1]!="719"){
        haokan[a[2]] += $2;
        haokanres +=$2
    }
    price[a[1]"#"a[2]] +=$2 
    res[a[1]] += $2
}END{
    for(i in price){
        split(i,idx,"#");
        printf("%s\t%0.0f\t%2.2f%\t%0.0f\n",i,price[i],price[i]/res[idx[1]]*100,res[idx[1]])
    }
    for (key in haokan){
        printf("%s\t%0.0f\t%2.2f%\t%0.0f\n","好看#"key,haokan[key],(haokan[key]-0)/haokanres*100,haokanres)
    }
}' ${file} &> "./data/"$dd"_"$week"_zongti_hangye"

input="./data/"$dd"_"$week"_zongti_hangye"
awk -F"\t" -v dd=$dd -v week=$week -v input=${input} 'BEGIN{
    OFS = "\t";
    while(getline<input){
        xiaofei[$1] = $2;
        zhanbi[$1] = $3;
        zongji[$1] = $4;
    }
}
{
    split($1,a,"#")
    k1 = "628#"a[2]
    k2 = "好看#"a[2]
    k3 = "669#"a[2]
    k4 = "687#"a[2]
    k5 = "689#"a[2]
    k6 = "675#"a[2]
    k7 = "719#"a[2]
    k8 = "855#"a[2]
    k9 = "856#"a[2]
    if(NR==1){ 
        print "总体",zongji[545"#"a[2]],"100.00%",zongji[k1],"100.00%",zongji[k2],"100.00%",zongji[k3],"100.00%",zongji[k4],"100.00%",zongji[k5],"100.00%",zongji[k6],"100.00%",zongji[k7],"100.00%",zongji[k8],"100.00%",zongji[k9],"100.00%"
    }
    if(a[1]=="545"){
        print a[2],xiaofei[$1],zhanbi[$1],xiaofei[k1],zhanbi[k1],xiaofei[k2],zhanbi[k2],xiaofei[k3],zhanbi[k3],xiaofei[k4],zhanbi[k4],xiaofei[k5],zhanbi[k5],xiaofei[k6],zhanbi[k6],xiaofei[k7],zhanbi[k7],xiaofei[k8],zhanbi[k8],xiaofei[k9],zhanbi[k9]
    }
}' ${input} | sort  -k2nr |iconv -c -f UTF8 -t GB18030 -s | head -20 &> "./data/"$dd"_"$week"/key_545_trade"



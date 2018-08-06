#!/bin/sh
#sunfuhao 

cat | ./dkf 32 | awk -F"\t" 'BEGIN{
    OFS = "\t";
    while(getline<"hangye_2"){
        hangye_list[$1] = $2
    }
    #while(getline<"./feeds_user_trade"){
    #    trade_id[$1] = $2
    #}
    while(getline<"./feedas_user_trade"){
        trade_id[$1] = $2
    }
}
{
    cmatch = $19;
    if (cmatch != 545 && cmatch!= 628 && cmatch!=669 && cmatch!=687 && cmatch!=689 && cmatch!=675) {
        next;
    }
    price = $16;
    userid = $8;
    tradeid= trade_id[userid]
    #trade_num = substr(tradeid,1,2)  
    #trade = hangye_list[trade_num]
    trade = hangye_list[tradeid]
    if(trade==""){
        trade="-" 
    }
    mt = match($57,"mt=([0-9]+)",a)
    key = cmatch"#"trade"#"a[1]
    print key,price
}' 

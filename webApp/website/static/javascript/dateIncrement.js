
//get todays date
n =  new Date();
y = n.getFullYear();
m = n.getMonth() + 1;
d = n.getDate();
j =0;
var leapYear; 
document.getElementById("date").innerHTML = m + "/" + d + "/" + y; // todays date
// leap year check
if (y%4 != 0){
    leapYear = false;
} else if (y%100 != 0 || y%400 == 0){
    leapYear = true;
} else {
    leapYear = false;
}

 for (let i = 1; i < 11; i++){
   // increment day
   // even months with 30 days
   if (m%2 == 0 && d+i <= 30 && m != 2){
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i-j) + "/" + y;
   // odd months with 31 days
    } else if (m%2 == 1 && d+i <= 31 && m != 2){
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i-j) + "/" + y;
   // feb that odd bastard
    } else if (m == 2 && d+i <= 28 && leapYear == false){
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i-j) + "/" + y;
       // feb in leap year
    } else if (m == 2 && d+i <= 29 && leapYear == true){
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i-j) + "/" + y;
    } 

    // increment month
    if (m%2 == 0 && d+i > 30 && m != 2 && m < 12){
       j=i;
       d = 1;
       m += 1;
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i-j) + "/" + y;
    } else if (m%2 == 1 && d+i > 31 && m < 12){
       j=i;
       d = 1;
       m += 1;
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i-j) + "/" + y;
    } else if (m == 2 && d+i > 28 && leapYear == false){
       j=i;
       d = 1;
       m += 1;
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i-j) + "/" + y;
    } else if ( m== 2 && d+i > 29 && leapYear == true){
       j=i;
       d = 1;
       m += 1;
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i-j) + "/" + y;
    }

    // increment year
    if (m == 12 && d+i > 31){
        m = 1
        d = 1
        y += 1
        document.getElementById("date"+i).innerHTML = m + "/" + d + "/" + y;
      }
 }

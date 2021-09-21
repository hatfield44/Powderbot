
//get todays date
n =  new Date();
y = n.getFullYear();
m = n.getMonth() + 1;
d = n.getDate();
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
   if (m%2 == 0 && d < 30 && m != 2){
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i) + "/" + y;
   // odd months with 31 days
    } else if (m%2 == 1 && d < 31 && m != 2){
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i) + "/" + y;
   // feb that odd bastard
    } else if (m == 2 && d < 28 && leapYear == false){
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i) + "/" + y;
       // feb in leap year
    } else if (m == 2 && d < 29 && leapYear == true){
       document.getElementById("date"+i).innerHTML = m + "/" + (d+i) + "/" + y;
    }
    // increment month
    if (m%2 == 0 && d == 30 && m != 2 && m < 12){
       d = 1
       m += 1
       document.getElementById("date"+i).innerHTML = (m) + "/" + d + "/" + y;
    } else if (m%2 == 1 && d == 31 && m < 12){
       d = 1
       m += 1
       document.getElementById("date"+i).innerHTML = (m) + "/" + d + "/" + y;
    } else if (m == 2 && d == 28 && leapYear == false){
       d = 1
       m += 1
       document.getElementById("date"+i).innerHTML = (m) + "/" + d + "/" + y;
    } else if ( m== 2 && d == 29 && leapYear == true){
       d = 1
       m += 1
       document.getElementById("date"+i).innerHTML = (m) + "/" + d + "/" + y;
    }
    // increment year
    if (m == 12 && d == 31){
        m = 1
        d = 1
        y += 1
    }
 }

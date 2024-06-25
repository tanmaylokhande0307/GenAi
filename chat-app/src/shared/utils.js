export const displayTime = () => {
    var str = "";
  
    var currentTime = new Date();
    var hours = currentTime.getHours();
    var minutes = currentTime.getMinutes();
    var seconds = currentTime.getSeconds();
  
    if (minutes < 10) {
      minutes = "0" + minutes;
    }
    if (seconds < 10) {
      seconds = "0" + seconds;
    }
    str += hours + ":" + minutes;
    // + ":" + seconds + " ";
    // if (hours > 11) {
    //   str += "PM";
    // } else {
    //   str += "AM";
    // }
    return str;
  };
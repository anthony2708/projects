setInterval(currentTime, 1000);

function currentTime() {
    let time = new Date(), dayName = time.getDay(), month = time.getMonth(), year = time.getFullYear();
    let date = time.getDate(), hour = time.getHours(), min = time.getMinutes(), sec = time.getSeconds();

    hour = hour < 10 ? "0" + hour : hour; min = min < 10 ? "0" + min : min;
    sec = sec < 10 ? "0" + sec : sec; date = date < 10 ? "0" + date : date;

    // Current time
    let currentTime = hour + ":" + min + ":" + sec;

    // Current Date
    var months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"];
    var week = ["Chủ nhật", "Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy"];
    var presentDay = week[dayName] + ", ngày " + date + " tháng " + months[month] + " năm " + year;

    $('#time').html(currentTime);
    $('#dayName').html(presentDay);
}

currentTime();
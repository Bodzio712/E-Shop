function validate() {
    if((validate_passwords() == true) && (validate_phone() == true) && (validate_email() == true)) {
        return true;
    } else {
        return false;
    }
}

function validate_passwords() {
    var pass = document.getElementById("password").value;
    var cpass = document.getElementById("cpassword").value;
    if (pass == cpass) {
        return true;
    } else {
        alert("Hasła nie są jednakowe");
        return false;
    }
}

function validate_phone() {
    var regex = /^\d{9}$/;
    var phone = document.getElementById("phone").value.toString();
    if(regex.test(phone) == true) {
        return true;
    } else {
        alert("Podaj numer telefonu w formacie: 111222333");
        return false;
    }

}

function validate_email() {
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/igm
    var email = document.getElementById("email").valueOf.toString();
        if(regex.test(email) == true) {
        return true;
    } else {
            alert("Adres email ma niepoprawny format");
            return false;
    }
}
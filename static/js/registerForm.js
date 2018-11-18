function validate() {
    if(validate_passwords() == True) {
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

}
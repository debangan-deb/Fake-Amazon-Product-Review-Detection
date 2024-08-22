function validation() {
    if (document.Formfill.Username.value == "") {
        document.getElementById("result").innerHTML = "!!PLEASE ENTER USERNAME!!";
        return false;
    }
    else if (document.Formfill.Username.value.length < 6) {
        document.getElementById("result").innerHTML = "!!USERNAME MUST HAVE ATLEAST 6 CHARACTERS!!";
        return false;
    }
    else if (document.Formfill.Email.value == "") {
        document.getElementById("result").innerHTML = "!!PLEASE ENTER YOUR EMAIL!!";
        return false;
    }
    else if(!document.Formfill.Email.value.match(/^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/)){
        document.getElementById("result").innerHTML = "!!PLEASE ENTER VALID EMAIL!!";
        return false;
    }
    else if (document.Formfill.Password.value == "") {
        document.getElementById("result").innerHTML = "!!PLEASE ENTER A PASSWORD!!";
        return false;
    }
    else if (document.Formfill.Password.value.length < 6) {
        document.getElementById("result").innerHTML = "!!PASSWORD MUST HAVE ATLEAST 6 CHARACTERS!!";
        return false;
    }
    else if (document.Formfill.ConfirmPassword.value == "") {
        document.getElementById("result").innerHTML = "!!PLEASE CONFIRM YOUR PASSWORD!!";
        return false;
    }
    else if (document.Formfill.Password.value !== document.Formfill.ConfirmPassword.value) {
        document.getElementById("result").innerHTML = "!!PASSWORDS DON'T MATCH!!";
        return false;
    }
    else if (document.Formfill.Password.value == document.Formfill.ConfirmPassword.value) {
        return true;
    }
}


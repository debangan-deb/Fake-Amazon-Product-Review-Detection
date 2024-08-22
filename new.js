function validation() {
    if (document.Formfill.Password.value == "") {
        document.getElementById("result").innerHTML = "!!PLEASE ENTER A NEW PASSWORD!!";
        return false;
    }
    else if (document.Formfill.Password.value.length < 6) {
        document.getElementById("result").innerHTML = "!!NEW PASSWORD MUST HAVE ATLEAST 6 CHARACTERS!!";
        return false;
    }
    else if (document.Formfill.ConfirmPassword.value == "") {
        document.getElementById("result").innerHTML = "!!PLEASE CONFIRM YOUR NEW PASSWORD!!";
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


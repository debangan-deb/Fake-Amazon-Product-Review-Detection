function validation(){
    if(document.Formfill.Username.value==""){
        document.getElementById("result").innerHTML="!!PLEASE ENTER USERNAME!!";
        return false;
    }
    else {
        return true;
    }
}


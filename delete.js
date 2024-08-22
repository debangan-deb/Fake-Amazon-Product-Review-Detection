function validation(){
    if(document.Formfill.Password.value==""){
        document.getElementById("result").innerHTML="!!PLEASE ENTER YOUR PASSWORD!!";
        return false;
    }   

    else{
        return true;
    }
}



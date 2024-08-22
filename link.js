function validation(){
    if(document.Formfill.Link.value==""){
        document.getElementById("result").innerHTML = "!!LINK CAN'T BE EMPTY!!";
        return false;
    }
    else if(!document.Formfill.Link.value.match(/^(?:https?:\/\/)?(?:www\.)?amazon\.[a-z]{2,3}\/(?:[^/]+\/)?(?:dp|gp\/product|ASIN)\/[a-zA-Z0-9]+/)){
        document.getElementById("result").innerHTML = "!!ONLY AMAZON PRODUCT LINKS ALLOWED!!"
        return false;
    }
    else{
        document.getElementById("result").innerHTML = " PLEASE WAIT! FILE WILL AUTO DOWNLOAD ON COMPLETION ";
        return true;
    }

}

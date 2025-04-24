const password=document.getElementById("password")
const confirm=document.getElementById("mdp")
const valid=document.getElementById("valid")

password.addEventListener('input',verifierMDP)
pass.addEventListener('input',verifierMDP)

function verifierMDP(){
    if(password.value != pass.value){
        valid.disabled=true
    }else{
        valid.disabled=false
    }
}

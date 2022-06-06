function loginid(){
    let userid = document.getElementById("exampleInputEmail1").value;
    if (userid == ""){
        alert("please give user id")
    }
    else{
        var url = ''
        fetch(url, {
            mathod:'POST',
            header:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': csrftoken,
            },
        body: JSON.stringify({  
                                'id':'Data to post',
                                'password': ''
                                }) 
    })
    .then(response => {
          return response.json() //Convert response to JSON
    })
    .then(data => {
    //Perform actions with the response data from the view
    })
    }
}
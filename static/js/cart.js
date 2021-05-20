var updateBtns = document.getElementsByClassName('update-cart')

// adding the event lestner to every add item  btn

for(var i = 0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log(productId, ' ', action)

        console.log('user ', user)

        //check if user is logged in or not
        if(user === 'AnonymousUser'){
            console.log('not logged in')
        }else{
            //if yes send the request to the server
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('hi user')
    //to wich viwe i will send data this case is the view i routed
    var url = '/update_item/'
    //fetch ajax request to the server
    fetch(url, {//to replace the form value quz there is no form
        method: 'POST',
        headers: {//the content will be in json format
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,//django csrf code in main.html
        },
        body: JSON.stringify({//this is the data converted to json format
            'productId': productId, 'action': action
        })
    })
    .then((response) => {//after we get the response(promis) process the json data
        return response.json()
    })
    .then((data) =>{//use the actual data
        console.log(data)
        location.reload()
    })
}
const cartValue = localStorage.getItem("cartValue");

function atc(){
    let c=document.getElementsByClassName('cartNumber')
    debugger
    let inc=Number(c[0].innerText)+1
    inc=String(inc)
    c.innerText=inc
    localStorage.setItem()
    console.log(inc)
}
let s=document.getElementsByClassName("p")
for (i=0;i<s.length;i++){
   console.log(s[i].childNodes[8].innerText)
   if (s[i].childNodes[8].innerText==="On The Way"){
        s[i].childNodes[10].childNodes[1].classList.add("otw")
    }
    s[i].childNodes[10].childNodes[1].classList.add(s[i].childNodes[8].innerText)
}

$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString()
    var elem=this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            document.getElementById('lenght').innerText=data.lenght
            elem.parentNode.remove()
        }
    })
})
$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var elm=this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id:id
        },
        success: function (data) {
            elm.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})
$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var elm=this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id:id
        },
        success: function (data) {
            elm.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})


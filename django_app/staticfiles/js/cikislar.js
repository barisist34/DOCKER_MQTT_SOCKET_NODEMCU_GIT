
function cikisAyarla(){
    var cikis1;
    if (document.getElementById("cikis1").value == "Aç")
        cikis1=True;
    else
        cikis1=false;
    $.ajax({        
        url: 'http://81.214.131.122:90/django_cikis_ayarla',
        // type: 'POST',
        type: 'GET',
        data:{
         cikis1:cikis1,
        //SicaklikKayit:SicaklikKayit,
        // csrfmiddlewaretoken: '{{ csrf_token }}',
        // dataType: "json",
        },
        // beforeSend: function (xhr){
        //   xhr.setRequestHeader('X-CSRFToken', csrftoken);
        // },
        success: function(response){
          //alert("arduino success girdi...");
          console.log("ajax success girdi...");
          console.log(response);
        //$('#test').html(response);
        console.log(response.No);
        var numara=response.No;
        console.log(typeof response.No);
        document.getElementById("cihaz-adi").innerHTML=String(response.CihazAdi);
        document.getElementById("cihaz-ip").innerHTML=String(response.CihazIp);
        document.getElementById("cihaz-port").innerHTML=String(response.CihazPort);
        document.getElementById("cihaz-sicaklik").innerHTML=String(response.CihazSicaklik);
        document.getElementById("cihaz-nem").innerHTML=String(response.CihazNem);
        document.getElementById("cihaz-voltaj").innerHTML=String(response.CihazVoltaj);

        },
                        failure: function() {
                    //alert("ajax reverse fail geldi");
                    console.log("ajax failure girdi...")
                      }               
    });
}
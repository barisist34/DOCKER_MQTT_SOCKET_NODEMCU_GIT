        ////////////////////////////////

        var my_ip = location.host; // 250812 server ip adresini gösterir
        //alert(my_ip);

        var alarm_id
        var output_no
        //output_no=parseInt(message_object["xo_n"])
        //output_no=parseInt(message_object_message["xo_n"])
        output_no=parseInt(message_object_message_json["xo_n"])
        console.log(`message_object_message_json["xo_n"]:${message_object_message_json["xo_n"]}`)
        console.log("output soket ajax girdi...")
        var cikis_degeri
      switch (output_no) {
      case 0:
              {
            alarm_id = 2
            //cikis_degeri = message_object["xo0"]
            cikis_degeri = message_object_message_json["xo0"]
              }
        break;
      case 1:
              {
            alarm_id = 3
            //cikis_degeri = message_object["xo00"]
            cikis_degeri = message_object_message_json["xo00"]
              }
        break;
      case 2:
              {
            alarm_id = 4
            //cikis_degeri = message_object["xo01"]
            cikis_degeri = message_object_message_json["xo01"]
              }
        break; 
      case 3:
              {
            alarm_id = 5
            //cikis_degeri = message_object["xo02"]
            cikis_degeri = message_object_message_json["xo02"]
              }
        break; 
      case 4:
              {
            alarm_id = 6
            //cikis_degeri = message_object["xo03"]
            cikis_degeri = message_object_message_json["xo03"]
              }
        break; 
        default:
        break;
            }


$.ajax({
    //url: 'http://81.214.131.122:90/django_cikis_ayarla',
    //url: 'http://{{cihazlar_erisim_ip}}:{{device_port}}/django_cikis_ayarla',
    //url: 'http://{{cihazlar_erisim_ip}}:{{device_port}}/addEventArduino',
    //url: 'http://localhost:9000/addEventArduino',
    //url: `http://${my_ip}/addEventArduino`, // back tick ile my_ip alındı
    url: `http://${my_ip}/app_monitor/addEventArduino`, // back tick ile my_ip alındı
    //url: 'http://192.168.1.42:{{device_port}}/django_cikis_ayarla',
    //url: 'http://192.168.1.215:{{device_port}}/django_cikis_ayarla', // VodafoneSmartUltra6
    //url: 'http://192.168.43.166:90/django_cikis_ayarla',
    // type: 'POST',
    type: 'GET',
    data: {
        //cikis_no=request.GET.get("cikis_no")
        cikis_degeri: cikis_degeri,
        device_id: xid, 
        //device_id: {{device_id}}, 
        alarm_id: alarm_id,
        //cikis0: cikis0,
        //cikis00: cikis00,
        //cikis01: cikis01,
        //cikis02: cikis02,
        //cikis03: cikis03,
        //butonno: butonno, // 250423 butono arduino_cikis_ayarla() gönderilecek
        //SicaklikKayit:SicaklikKayit,
        // csrfmiddlewaretoken: '{{ csrf_token }}',
        // dataType: "json",
    },
    // beforeSend: function (xhr){
    //   xhr.setRequestHeader('X-CSRFToken', csrftoken);
    // },
    success: function (response) {
        //alert("arduino success girdi...");
        console.log("addEventArduino ajax success girdi...");
        //console.log(response);

    },
    failure: function () {
        //alert("ajax reverse fail geldi");
        console.log("ajax failure girdi...")
    }
}); 


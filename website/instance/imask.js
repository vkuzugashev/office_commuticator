//1 пример
$(function(){
  $("#phone1").mask("8(999) 999-9999");
});
//2 пример
$("#date").mask("99.99.9999", {placeholder: "дд.мм.гггг" });
$("#index").mask("999999", {placeholder: " " });
//3
$("#phone3").mask("8(999) 999-9999", {
  completed: function(){ alert("Вы ввели номер: " + this.val()); }
});
//4
$("#number").mask("0.9?9");
//5
$.mask.definitions['~']='[+-]';
$("#number2").mask("~9.99");
$.mask.definitions['h']='[A-Fa-f0-9]';
$("#color").mask("#hhhhhh");

  $(function() {
    function maskPhone() {
      var country = $('#country option:selected').val();
      switch (country) {
        case "ru":
          $("#phone").mask("+7(999) 999-99-99");
          break;
        case "ua":
          $("#phone").mask("+380(999) 999-99-99");
          break;
        case "by":
          $("#phone").mask("+375(999) 999-99-99");
          break;          
      }    
    }
    maskPhone();
    $('#country').change(function() {
      maskPhone();
    });
  });
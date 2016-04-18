

   $(function() {
      $('#btnSignUp').click(function() {
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                $(response).appendTo('#error'); 
                //window.location.href = "/CUSignIn"
            },
            error: function(error) {
                console.log(error);
                $(error).appendTo('#error'); 
                //$('#error').show(); 
            }
        });
      });
   });


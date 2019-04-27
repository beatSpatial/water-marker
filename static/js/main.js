$(function(){

  function renderScaffold(data){

    $('#js-scaffold-options').select2({
        theme: "bootstrap",
        placeholder: 'Choose Scaffold',
        allowClear: true,
        data: data['scaffold']

    })
    $('#js-scaffolds').show()

  }


  function renderStudents(year, cohort, class_num){
    $('#js-student-options').select2({
        theme: "bootstrap",
        placeholder: 'Ctrl to multi-select students',
        allowClear: true,
        tags: true,
        ajax: {
            url: $('#js-students').attr('js-get-students-url'),
            async: true,
            type: "GET",
            dataType: 'json',
            data: {
                'year': year,
                'cohort': cohort,
                'class_num': class_num
                },
            success: function(result){
               
                return result

            },
            error : function(xhr,errmsg,err) {
                // Show an error
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        }
    })
  }

  function renderClassOptions(year, cohort){
    $('#js-class-options').empty()
    $.ajax({
      url: $("#js-class-options").attr('js-get-class-options-url'),
      async: true,
      type: "GET",
      data: {
          'year': year,
          'cohort': cohort
          },
      dataType: 'json',
      success: function(data){
          var classes = data.classes
          options = ""
          $.each(classes, function () {
              options += `<div class="form-check">
              <input class="form-check-input" type="radio" name="js-class-options"
                id="${this.id}" value="${this.id}">
              <label class="form-check-label" for="${this.id}">${this.display}</label>
              </div>`
              })
          $('#js-class-options').append(options)
          $('#js-classes').show()
          $('input[name="js-class-options"]').change(function(){
            var year = $('input[name="js-year-options"]:checked').val()
            var cohort =$('input[name="js-cohort-options"]:checked').val()
            var class_num = $(this).val()
            renderStudents(year, cohort, class_num)
            renderScaffold(data)
            $('#js-students').show()
          })
      },
      error : function(xhr, errmsg, err) {

          // add error to the dom
          $('#js-results').html("<div class='alert-box alert radius' data-alert>"+
          "Oops! There has been an error.</div>");

          // Provide error detail to the console
          console.log(xhr.status + ": " + xhr.responseText);
      }
    })
  }
  
  function renderCohortOptions(year){
    console.log('Render Cohort options')
    $('#js-cohort-options').empty()
    $.ajax({
      url: $("#js-cohort-options").attr('js-get-cohort-options-url'),
      async: true,
      type: "GET",
      data: {
          'year': year,
          },
      dataType: 'json',
      success: function(result){
        options = ""
        $.each(result, function () {
            options += `<div class="form-check">
            <input class="form-check-input" type="radio" name="js-cohort-options"
              id="${this.id}" value="${this.id}">
            <label class="form-check-label" for="${this.id}">${this.display}</label>
            </div>`
            })
        $('#js-cohort-options').append(options)
        $('#js-cohorts').show()
        $('input[name="js-cohort-options"]').change(function(){
          
          var year = $('input[name="js-year-options"]:checked').val()
          var cohort = $(this).val()
          console.log(year, cohort)
          renderClassOptions(year, cohort)

        })
      },
      error : function(xhr, errmsg, err) {

        // add error to the dom
        $('#js-results').html("<div class='alert-box alert radius' data-alert>"+
        "Oops! There has been an error.</div>");

        // Provide error detail to the console
        console.log(xhr.status + ": " + xhr.responseText);
      }
    })
     
  }


  $('input[name="js-year-options"]').change(function(){
    var year = $(this).val()

    renderCohortOptions(year)
  });

  $("#watermark").click(function(){
    var students = $('#js-student-options').select2('data');
    var scaffold = $('#js-scaffold-options').select2('data');
    var std_ids = "";
    $(students).each(function(i){
        std_ids += `${students[i].id} `;
    });
    $.ajax({
      url: $("#watermark").attr('watermark-url'),
      async: true,
      type: "GET",
      data: {
          'scaffold': scaffold[0].id,
          'students': std_ids
          },
      xhrFields: {
            responseType: 'blob'
        },
      success: function(data){
        var a = document.createElement('a');
            var url = window.URL.createObjectURL(data);
            a.href = url;
            a.download = 'myfile.pdf';
            a.click();
            window.URL.revokeObjectURL(url);
        },
      error : function(xhr, errmsg, err) {

        // add error to the dom
        $('#js-results').html("<div class='alert-box alert radius' data-alert>"+
        "Oops! There has been an error.</div>");

        // Provide error detail to the console
        console.log(xhr.status + ": " + xhr.responseText);
      }
    })


  })
 
});
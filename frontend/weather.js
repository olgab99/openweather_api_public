SERVER_URL = 'http://127.0.0.1:5000/api/';  //replace with backend server url
sel_city_id ='';
sel_country_code='';

$(document).ready(function(){
             $(".coords").bind("keydown", function (event) {
                      coordsOnlyKeyDown(event);
              });

         getSupportedCountries();
});

        function getWeatherByCity(){
            city = $('#city').val().trim();
            if (alphanumeric(city) == false){
                   alert("Invalid city name");
                   return;
            }

            url = SERVER_URL + 'weather?city=' + city + get_units();
            capt = 'City: ' + city;
            fetch_data(url, populate_weather, capt);
        }

         function getWeatherByZip(){
            var zip = $('#zip').val().trim();
            if (zip == '' || alphanumeric(zip) == false){
                   alert("Invalid zip code");
                   return;
            }

            url = SERVER_URL + 'weather?zip=' + zip + get_units();
            fetch_data(url, populate_weather, 'Zipcode: ' + zip);
        }

        function get_units(){
            var units_val = $("input[name='units']:checked").val();
            return '&units=' + units_val;
        }

         function getWeatherByCoords(){
            lon = $('#lon').val();
            lat = $('#lat').val();
            url = SERVER_URL + 'weather?lat=' + lat +'&lon=' + lon + get_units();
           fetch_data(url, populate_weather, 'Coordinates: lon='+ lon + " lat=" + lat);
         }

        function fetch_data(url, callback, caption) {
            fetch(url)
              .then(
                function(response) {
                  if (response.status !== 200) {
                    alert('Looks like there was a problem. Status Code: ' +
                      response.status);
                    return;
                  }
                  response.json().then(function(data) {
                    callback(data);
                    setCaption(caption);
                  });
                }
              )
              .catch(function(err) {
                console.log('Fetch Error :-S', err);
                alert("Error processing request.")
              });
        }

        function setCaption(caption_text){
            $("#caption").html(caption_text);
        }

        function getSupportedCountries(){
            const url = SERVER_URL + 'countries';
            fetch_data(url, populate_country_list, '');
        }

        function get_supported_cities(country) {
            if (country == ''){
                alert("please select Country");
                return;
            }
            const url = SERVER_URL + 'cities?country='+ country;
            fetch_data(url, populate_city_list, '');
         }

        function populate_country_list(res){
            var dd =  $("#selcountry-menu");
            dd.empty();
             $("#selcity-menu").empty();
             $("#but-get-weather").prop('disabled', false);

              var d ='';
              $.each(res.data, function (index, entry) {
                d += '<a class="dropdown-item" href="#" id="' + entry.code + '" onclick="selectCountry(\'' + entry.code +'\', \'' + entry.country + '\');return false;">' +  entry.country  + '</a>';
              });
              dd.append(d);
        }

        function populate_city_list(res){
             var dd = $("#selcity-menu");
             dd.empty();

             var d ='';
              $.each(res.data, function (index, entry) {
                d += '<a class="dropdown-item" href="#" id="' + entry.id + '" onclick="selectCity(\'' + entry.id +'\', \'' + entry.city + '\');return false;">' +  entry.city  + '</a>';
              });
              dd.append(d);
              $("#but-get-weather").css("visibility", "visible");
        }

        function selectCity(id, city) {
            sel_city_id = id;
            $("#selcitybut").html(city +'<span class="caret"></span>');
        }

        function selectCountry(code, country) {
            sel_country_code = code;
            get_supported_cities(sel_country_code);
            $("#selcountrybut").html(country +'<span class="caret"></span>');
        }

        function getWeather() {
           if (sel_city_id == ''){
                alert("please select City");
                return;
           }

            const url = SERVER_URL + 'weather?id=' + sel_city_id + get_units();
            fetch_data(url, populate_weather, 'City id: ' + sel_city_id);

        }

        function populate_weather(res){
             $("#result").empty();

             str = '';
             $.each(res.data, function (index, entry){
                // category, data
                //append category
                str += '<h4>' +entry.category_title + '<h4>';
                // iterate items
                $.each(entry.data, function (ind, record) {
                    str += '<p class="paddleft"><span style="color: blue;">' + record.title + '</span>: ' + record.value + '</p>';
                });

             });

             $("#result").append(str);

        }

        function coordsOnlyKeyDown(event){
            if ( event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 ||
                event.keyCode == 13 ||  event.keyCode == 45 || event.keyCode == 190 || event.keyCode == 173 ||
                event.keyCode == 109 || event.keyCode == 110 ||
                // Allow: Ctrl+A
                (event.keyCode == 65 && event.ctrlKey === true) ||

                // Allow: Ctrl+C
                (event.keyCode == 67 && event.ctrlKey === true) ||

                // Allow: Ctrl+V
                (event.keyCode == 86 && event.ctrlKey === true) ||

                // Allow: home, end, left, right
                (event.keyCode >= 35 && event.keyCode <= 39)) {
                // let it happen, don't do anything
                return;
            } else {
                // Ensure that it is a number, dot or - and stop the keypress
                if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                    event.preventDefault();
                }
            }
       }
        // verify alphanumeric, dash or space
        function alphanumeric(inputtxt)
        {
             var letterNumber = /^[0-9a-zA-Z- ]+$/;
             if(inputtxt.match(letterNumber))
              {
               return true;
              }
            else
              {
               return false;
              }
         }

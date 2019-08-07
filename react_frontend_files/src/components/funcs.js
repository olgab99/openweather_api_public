function fetchDataFromServer(url, callback, country, city){
    let result = [];
    fetch(url)
          .then((response) => {
            if (response.status !== 200) {
                alert('Looks like there was a problem. Status Code: ' +
                  response.status);
                return;
              }
              return response.json();
          })
          .then(res => {
                console.log("data");
                
                result = res.data.map((item) => {
                    return item
                });
                console.log(result);
                callback(result, country, city);
          }).catch(error => {
            console.log(error);
            alert("Error fetching data: " + error)
          });            
}

export {fetchDataFromServer};
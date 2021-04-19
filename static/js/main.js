function run_scraper(){
    $.ajax({
        url:'scrape',
        type:'get',
        success: function(response){
            console.log("success")
            document.getElementById("display").innerHTML = response.result
        }
    })
}

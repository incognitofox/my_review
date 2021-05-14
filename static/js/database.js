function show_database(){
 console.log("database")
 $.ajax({
     url: 'database',
     type: 'post',
     success: function(response){
        console.log("Success!")
        csv = response.csv;
        var table_data = Papa.parse(csv,{header: true,})
        table_data = table_data.data
        var columns = []
        var header = table_data[0]
        console.log(header)
        for(const prop in header){
           var column;
           console.log(prop)
           if(typeof(header[prop]) == 'string'){
               column = {
                   title: prop,
                   field: prop,
                   headerFilter: 'input',
               }
           }
           if(typeof(header[prop]) == 'number'){
               column = {
                   title: prop,
                   field: prop,
                   headerFilter: minMaxFilterEditor,
                   headerFilterFunc: minMaxFilterFunction,
                   headerFilterLiveFilter: false
                }
           }
           columns.push(column)
        }
        console.log(columns)
        var table = new Tabulator("#database_left",
            { 
              data: table_data,
              columns: columns,
              movableColumns: true,
              movableRows: true,
              movableRowsConnectedElements: "#database_right",
              movableRowsElementDrop: database_drag,
              pagination:"local",
              paginationSize:25,
              paginationSizeSelector:[5, 10, 25, 50, 100, 1000],
              rowClick: database_click
            });
        cols = table.getColumns()
        console.log(cols)
      //  document.getElementById("charts").style.display = "block";
        table.redraw();
     }
 })
}

function database_drag(e, element, row){
   var table_display = document.createElement("li");
   table_display.textContent = row.getData().id;
   console.log(row.getData().id)
   element.appendChild(table_display);
}

function database_click(e, row){
   data = row.getData()
   header = data['_id']
   text = "<h2>" + header + "</h2><table>"
   for(const prop in data){
      if(prop != '_id')
        text += "<tr><td>" + prop + "</td><td>" + data[prop] + "<td></tr>"
   }
   text += "</table>"
   console.log(text)
   document.getElementById("database_right").innerHTML = text;
   console.log(row.getData())
}

function minMaxFilterEditor(cell, onRendered, success, cancel, editorParams){

    var end;

    var container = document.createElement("span");

    var start = document.createElement("input");
    start.setAttribute("type", "number");
    start.setAttribute("placeholder", "Min");
    start.setAttribute("min", 0);
    start.setAttribute("max", 100);
    start.style.padding = "4px";
    start.style.width = "50%";
    start.style.boxSizing = "border-box";

    start.value = cell.getValue();

    function buildValues(){
        success({
            start:start.value,
            end:end.value,
        });
    }

    function keypress(e){
        if(e.keyCode == 13){
            buildValues();
        }

        if(e.keyCode == 27){
            cancel();
        }
    }

    end = start.cloneNode();
    end.setAttribute("placeholder", "Max");

    start.addEventListener("change", buildValues);
    start.addEventListener("blur", buildValues);
    start.addEventListener("keydown", keypress);

    end.addEventListener("change", buildValues);
    end.addEventListener("blur", buildValues);
    end.addEventListener("keydown", keypress);


    container.appendChild(start);
    container.appendChild(end);

    return container;
 }

function minMaxFilterFunction(headerValue, rowValue, rowData, filterParams){
        if(rowValue){
            if(headerValue.start != ""){
                if(headerValue.end != ""){
                    return rowValue >= headerValue.start && rowValue <= headerValue.end;
                }else{
                    return rowValue >= headerValue.start;
                }
            }else{
                if(headerValue.end != ""){
                    return rowValue <= headerValue.end;
                }
            }
        }

    return true;
}

$(document).ready(function(){

    $("#collapse").on("click",function(){
    
        $("#sidebar").toggleClass("active");
        $(".fa-align-left").toggleClass("fa-chevron-circle-right");

    })
})
    
    // 點擊後跳出dialog
    function showDialog(){  
        dialog.style.display="block";
    }
    // 點擊後關閉dialog
    function closeDialog(){
        dialog.style.display = "none";
    }


    // 動態新增進度敘述
    
    var content = document.getElementById("fix-list");
  

    fetch('/fix_page')
        .then(response => response.json())
        .then(fixlist => {

            // 在控制台上顯示獲取的資料
            console.log(fixlist);
            console.log(fixlist.length);
            // console.log(fixlist[1][0]);

            // 動態新增div
            for (let i = fixlist.length-1; i >= 0; i--) {
                const fixbox = document.createElement('div');
                fixbox.setAttribute('class', 'fixbox');
                // probox.setAttribute('onclick', 'showDialog();');

            
                // 新增item欄位
                const item = document.createElement('span');
                item.setAttribute('class', 'item');
                item.style.paddingRight = "15%";

                // 新增dorm欄位
                const dorm = document.createElement('span');
                dorm.setAttribute('class', 'dorm');
                dorm.style.paddingRight = "15%";

                // 新增place欄位
                const place = document.createElement('span');
                place.setAttribute('class', 'place');

                // 新增number欄位
                const  number= document.createElement('span');
                number.setAttribute('class', 'number');
                number.style.paddingRight = "15%";

                // 新增subtimes欄位
                const subtimes = document.createElement('span');
                subtimes.setAttribute('class', 'subtimes');

                // 新增explain欄位
                const explain = document.createElement('span');
                explain.setAttribute('class', 'explain');

                // 新增status欄位
                const status = document.createElement('span');
                status.setAttribute('class', 'status');
                status.style.paddingRight = "15%";

                // 新增name欄位
                const name = document.createElement('span');
                name.setAttribute('class', 'name');
                name.style.paddingRight = "15%";
                
                

                dorm.innerHTML = fixlist[i][0];
                name.innerHTML = fixlist[i][1];
                // 判別fix_subject和other_fix_subject
                if (fixlist[i][2] == "其他"){
                    item.innerHTML = fixlist[i][8];
                }
                else{
                    item.innerHTML = fixlist[i][2];
                }
                place.innerHTML = fixlist[i][3];
                number.innerHTML = fixlist[i][4];
                status.innerHTML = fixlist[i][5];
                subtimes.innerHTML = fixlist[i][6];
                explain.innerHTML = '說明: <br/>' + fixlist[i][7];


                // 將div新增到指定的div中,把指定內容放入div(probox內的內容)
                content.appendChild(fixbox);
                
                fixbox.appendChild(dorm);
                fixbox.appendChild(name);
                fixbox.appendChild(item);
                // fixbox.appendChild(place);
                fixbox.appendChild(number);
                // fixbox.appendChild(subtimes);
                // fixbox.appendChild(explain);
                fixbox.appendChild(status);

                const divs = document.querySelectorAll('.fixbox');
               
                
                // 為每個被新增的 div 綁定一個點擊事件
                divs.forEach((div) => {
                div.addEventListener('click', () => {
                    // console.log(div.innerHTML);
                    // 顯示 dialog
                    showDialog();
                    // 將被點擊的 div 的內容顯示在 dialog 中
                    const boxtitle = document.createElement('p');
                    boxtitle.setAttribute('class', 'boxtitle');
                    boxtitle.innerHTML = '維修進度' + '<br>' + '<br>';
                    if (fixlist[i][2] == "其他"){
                        fixitem = fixlist[i][8];
                    }
                    else{
                        fixitem = fixlist[i][2];
                    }

                    const boxitems = `
                    <form action="/fixlist_change" method="post">
                        <p class="dorm" name="dorm">棟別: ${fixlist[i][0]}</p>
                        <p class="name" name="name">姓名: ${fixlist[i][1]}</p>
                        <p class="item" name="item">項目: ${fixitem}</p>
                        <p class="place" name="place">地點: ${fixlist[i][3]}</p>
                        <p class="number" name="number">床位: ${fixlist[i][4]}</p>
                        <p><span class="status" name="time">維修進度: ${fixlist[i][6]}</span><span class="status" name="status"> - ${fixlist[i][5]}</span></p>
                        <p class="explain" status="explain">說明: ${fixlist[i][7]}</p>
                        <p class="progress_explain mb-3">
                            <label for="progress_explain" class="form-label">進度說明</label>
                            <textarea class="form-control" name="progress_explain" id="progress_explain" rows="2" placeholder="進度說明"></textarea>
                        </p>
                        
                        <select class="status_select">
                            <option value="待確認">待確認</option>
                            <option value="已確認">已確認</option>
                            <option value="處理中">處理中</option>
                            <option value="待料中">待料中</option>
                            <option value="已完工">已完工</option>
                            </select><br/>
                        <div>
                            <button type="button" class="btn btn-outline-primary">完成</button>
                        </div>
                    </form>
                    `;
                    

                    const dialogContent = document.getElementById('dialog_content');
                    dialogContent.innerHTML = boxtitle.innerHTML + boxitems;
                });
                });

                const closeButton = document.getElementById('close');
                closeButton.addEventListener('click', () => {
                    closeDialog();
                });
            }
        })
        .catch(error => {
            console.log(error);
        });


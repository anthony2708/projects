const addPlayer = document.querySelector('.addPlayer');
const listPlayers=$('#players');
let i = 1;

addPlayer.onclick = function (e) { 
        e.preventDefault();
        listPlayers.append(`<div class="player${++i}"> <span class="input-group mb-1 mt-1">Cầu thủ ${i}</span>` +
                '<div class="input-group mb-3">' +

                  '<span class="input-group-text">Họ và tên</span>' +
                  `<input type="text" class="form-control col-9 bg-secondary" name="namePlayer${i}">` +
                  '<span class="input-group-text">Số áo</span>' +
                  `<input type="text" class="form-control col-1 bg-secondary" name="number${i}">` +
                  `<select class="form-select" id="age-Selection" name="age${i}">` +
                    '<option selected value="">Độ tuổi...</option>' +
                    '<option value="16">16</option>' +
                    '<option value="17">17</option>' +
                    '<option value="18">18</option>' +
                    '<option value="19">19</option>' +
                    '<option value="20">20</option>' +
                    '<option value="21">21</option>' +
                    '<option value="22">22</option>' +
                    '<option value="23">23</option>' +
                  '</select>' +

                  `<select class="form-select" id="positon-Selection" name="position${i}">` +
                    '<option selected value="">Vị trí...</option>' +
                    '<option value="ST">Tiền đạo</option>' +
                    '<option value="CM">Tiền vệ</option>' +
                    '<option value="CB">Hậu vệ</option>' +
                    '<option value="GK">Thủ môn</option>' +
                  '</select>' +

                `<button class="btn btn-primary deletePlayer${i}">Xóa</button></div></div>`);
          for(let j = 1; j <= i; j++) {
            const deletePlayer = document.querySelector(`.deletePlayer${j}`); 
            const player = document.querySelector(`.player${j}`);
            deletePlayer.onclick = function (e) {
              e.preventDefault();
              player.remove();
              i--;
              const players = document.querySelectorAll('div[class^="player"]');
              for(let j = 0; j < players.length; j++) {
                players[j].className=`player${j+1}`;
                players[j].querySelector('span[class="input-group mb-1 mt-1"]').innerText= `Cầu thủ ${j+1}`;
                players[j].querySelector('button[class^="btn btn-primary deletePlayer"]').className=`btn btn-primary deletePlayer${j+1}`;
                players[j].querySelector('input[name^="namePlayer"]').name= `namePlayer${j+1}`;
                players[j].querySelector('input[name^="number"]').name= `number${j+1}`;
                players[j].querySelector('select[name^="age"]').name= `age${j+1}`;
                players[j].querySelector('select[name^="position"]').name= `position${j+1}`;
              };
            };
          };    

      };
      const deletePlayer = document.querySelector(`.deletePlayer1`);
      const player = document.querySelector(`.player1`);
      deletePlayer.onclick = function (e) {
          e.preventDefault();
          player.remove();
          i--;
      };



      const addCoachOrSupport = document.querySelector('.addCoachOrSupport');
      const listCoachOrSupport=$('#CoachOrSupport');
      let k = 1;

      addCoachOrSupport.onclick = function (e) { 
        e.preventDefault();
        listCoachOrSupport.append(`<div class="CoachOrSupport${++k}"> 

                                                          <span class="input-group mb-1 mt-1">Thành viên ${k}</span>
                                                          <div class="input-group mb-3">

                                                            <span class="input-group-text">Họ và tên</span>
                                                            <input type="text" class="form-control bg-secondary col-9" name="nameCoachOrSupport${k}">

                                                            <select class="form-select col-3" id="role-Selection" name="role${k}">
                                                              <option selected value="">Vai trò...</option>
                                                              <option value="HLVT">HLV Trưởng</option>
                                                              <option value="HLVP">HLV Phó</option>
                                                              <option value="HC">Hậu cần</option>
                                                            </select>

                                                            <button class="btn btn-primary deleteCoachOrSupport${k}">Xóa</button>

                                                          </div>`);
          for(let j = 1; j <= k; j++) {
            const deleteCoachOrSupport = document.querySelector(`.deleteCoachOrSupport${j}`); 
            const CoachOrSupport = document.querySelector(`.CoachOrSupport${j}`);
            deleteCoachOrSupport.onclick = function (e) {
              e.preventDefault();
              CoachOrSupport.remove();
              k--;
              const players = document.querySelectorAll('div[class^="CoachOrSupport"]');
              for(let j = 0; j < players.length; j++) {
                  players[j].className=`CoachOrSupport${j+1}`;
                  players[j].querySelector('span[class="input-group mb-1 mt-1"]').innerText= `Thành viên ${j+1}`;
                  players[j].querySelector('button[class^="btn btn-primary deleteCoachOrSupport"]').className=`btn btn-primary deleteCoachOrSupport${j+1}`;
                  players[j].querySelector('input[name^="nameCoachOrSupport"]').name= `nameCoachOrSupport${j+1}`;
                  players[j].querySelector('select[name^="role"]').name= `role${j+1}`;
              };
            };
          };    
      };
      const deleteCoachOrSupport = document.querySelector(`.deleteCoachOrSupport1`);
      const CoachOrSupport = document.querySelector(`.CoachOrSupport1`);
      deleteCoachOrSupport.onclick = function (e) {
          e.preventDefault();
          CoachOrSupport.remove();
          k--;
      };

      const submitBtn = document.querySelector('.submit-btn');
      submitBtn.onclick = function (e) {
        const players = document.querySelectorAll('div[class^="player"]');
        const warning1 = document.querySelector('.warningForm1');
        const warning2 = document.querySelector('.warningForm2');
        let check1 = 0;
        let check2 = 0;
        if(players.length<11) {
          e.preventDefault();
          warning1.innerHTML = `<p class="text-danger" >*Bạn phải có ít nhất 11 cầu thủ trong đội hình</p>`;
          check1 = 1;
        }
        const Coach = document.querySelector('option[value="HLVT"]');
        if(!Coach.selected) {
          e.preventDefault();
          warning2.innerHTML = `<p class="text-danger">*Bạn phải có ít nhất 1 HLV trưởng</p>`;
          check2 = 1;
        } 
        if(check1==1 && check2==0) {
          e.preventDefault();
          warning2.innerHTML = ``;
        }
        if(check1==0 && check2==1) {
          e.preventDefault();
          warning1.innerHTML = ``;
        }
      }
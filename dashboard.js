//Check for indentation errors in this js code
function showPopup() {
    const popup = document.getElementById('popup');
    const cards1 = document.querySelector('.cards1');
    popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
    if (popup.style.display === 'block') {
      const popupWidth = popup.offsetWidth;
      cards1.style.width = `calc(100% - (${popupWidth}px + 40px))`;}
    else {
      cards1.style.width = 'auto';
      }
    }
  
    function closePopup() {
      const popup = document.getElementById('popup');
      const cards1 = document.querySelector('.cards1');
      popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
      if (popup.style.display === 'block') {
          const popupWidth = popup.offsetWidth;
          cards1.style.width = `calc(100% - (${popupWidth}px + 40px))`;
      } else {
          cards1.style.width = 'auto';
      }
    }
    function sharefile(){
      alert("File shared");
    }
    function newchat(){
      alert("new chat added");
    }
  
    function toggleNav(nav) {
      const dashboardBtn = document.querySelector('.nav-btn:nth-child(1)');
      const chatBtn = document.querySelector('.nav-btn:nth-child(2)');
  
      if (nav === 'dashboard') {
        dashboardBtn.classList.add('active');
        chatBtn.classList.remove('active');
      } else if (nav === 'chat') {
        chatBtn.classList.add('active');
        dashboardBtn.classList.remove('active');
      }
    }
  
  function toggleTabs(tab) {
    const filesBtn = document.querySelector('.tabs button:nth-child(1)');
    const sharedBtn = document.querySelector('.tabs button:nth-child(2)');
    const receivedBtn = document.querySelector('.tabs button:nth-child(3)');
  
    if (tab === 'files') {
      filesBtn.classList.add('active');
      sharedBtn.classList.remove('active');
      receivedBtn.classList.remove('active');
    } else if (tab === 'shared') {
      sharedBtn.classList.add('active');
      filesBtn.classList.remove('active');
      receivedBtn.classList.remove('active');
    } else if (tab === 'received') {
      receivedBtn.classList.add('active');
      filesBtn.classList.remove('active');
      sharedBtn.classList.remove('active');
    }
  }
  
  // Add event listeners to the tabs buttons
  document.querySelectorAll('.tabs button').forEach((button, index) => {
    button.addEventListener('click', () => {
      if (index === 0) {
        toggleTabs('files');
      } else if (index === 1) {
        toggleTabs('shared');
      } else if (index === 2) {
        toggleTabs('received');
      }
    });
  });
  
  function sortTable(n) {
      var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
      table = document.querySelector(".table");
      switching = true;
      dir = "asc";
      var th = table.rows[0].cells[n];
      var arrow = th.querySelector('.arrow');
      if (!arrow) {
          arrow = document.createElement('span');
          arrow.className = 'arrow';
          th.appendChild(arrow);
      }
      while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
          shouldSwitch = false;
          x = rows[i].getElementsByTagName("TD")[n];
          y = rows[i + 1].getElementsByTagName("TD")[n];
          if (dir == "asc") {
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
              shouldSwitch = true;
              break;
            }
          } else if (dir == "desc") {
            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
              shouldSwitch = true;
              break;
            }
          }
        }
        if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          switchcount++;
        } else {
          if (switchcount == 0) {
            if (dir == "asc") {
              dir = "desc";
              switching = true;
              arrow.textContent = '\u2193';
            } else {
              dir = "asc";
              switching = true;
              arrow.textContent = '\u2191';
            }
          } else {
            // reset the arrow when switching is done
            if (dir == "asc") {
              arrow.textContent = '\u2191';
            } else {
              arrow.textContent = '\u2193';
            }
          }
          // Remove arrow from other table headers
          var ths = table.rows[0].cells;
          for (var j = 0; j < ths.length; j++) {
            if (j != n) {
              var otherArrow = ths[j].querySelector('.arrow');
              if (otherArrow) {
                otherArrow.textContent = '';
              }
            }
          }
        }
      }
    }
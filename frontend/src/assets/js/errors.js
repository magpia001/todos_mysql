// textarea에 공백일 경우 경고창 띄우기
// let task = document.getElementById("task");
// let add_task = document.getElementById("add_task")
// add_task.addEventListener("click", (e) =>{
//   if (task.value == "") {
//     alert("입력한 TODO가 없습니다.");
//     // submit 방지함
//     e.preventDefault();
//     return false;
//   }
// })

// 입력값이 없는 경우 예외처리
function empty_check(ele_data) {
  // textarea에 공백일 경우 경고창 띄우기
    if (ele_data == "") {
      return "입력한 TODO가 없습니다.";
    }
}

export default empty_check


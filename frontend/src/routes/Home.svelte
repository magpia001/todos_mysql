 <script>
import {link, push} from 'svelte-spa-router'
let todos = []
let _todo  // 수정할 todo 저장
let task =''
let completed = false

let task_edit = false   // task 수정상태 체크
// $task_edit = false

const base_url = "http://127.0.0.1:9000/todo"


// task 목록 실행 함수
function get_todo_list() {
    const url = base_url + "/list"
    // 비동기 get 실행(primise 객체 처리)
    fetch(url).then((response) => {
        response.json().then((json) => {
          todos = json
            console.log(todos)
        })
    })
}  
get_todo_list()

// task 추가 함수
function add_todo(event){
  event.preventDefault()
  console.log(task)
  if (task == "") {
      alert("입력한 TODO가 없습니다.");
      return false;
  }

  // 비동기 post 실행(primise 객체 처리)
  const url = base_url + "/add"
  let data = {task: task}
  let params = {
    method: 'POST', 
    headers: {
      "Content-Type": "application/json",
    },
    // json 데이터를 문자열 형식으로 변환
    body: JSON.stringify(data)
  };
  fetch(url, params).then((response) => {
    response.json()}).then((json) => {
      // 홈 실행
      task=''
      get_todo_list()
    })
}

// 수정할 task 가져오기
function get_edit_todo(event, todo_id) {
  // a 태그의 기본 이벤트 속성을 방지
  event.preventDefault()
  const url = base_url + "/edit/" + todo_id
  // console.log(url)

  // 비동기 get 실행(primise 객체 처리)
  fetch(url).then((response) => {
    response.json().then((json) => {
      _todo = json
      console.log(_todo)
      task = _todo.task
      completed = _todo.completed

      // task 편집모드 전환
      task_edit = true
    })
  })
}  

// 수정한 task 서버에 적용하기
function update_edit_todo(event, _todo_id) {
  const url = base_url + "/update/"
  console.log(url, "수정id :", _todo_id)

  event.preventDefault()
  if (task == "") {
    alert("입력한 TODO가 없습니다.");
    return false;
  }

  // 비동기 post 실행(primise 객체 처리)
  let data = {id: _todo_id, task: task, completed: completed}
  let params = {
    method: 'PUT', 
    headers: {
      "Content-Type": "application/json",
    },
    // json 데이터를 문자열 형식으로 변환
    body: JSON.stringify(data)
  };
  fetch(url, params).then((response) => {
    response.json()}).then((json) => {

      // 전체 tast 목록 자져오기 함수 호출
      get_todo_list()

      // 변수 초기화
      task=''
      completed = false
      task_edit = false
    })
}

// task 삭제 함수
function delete_todo(event, todo_id) {
  event.preventDefault()
  const url = base_url + "/delete/" + todo_id
  // console.log(url)

  // 비동기 get 실행(primise 객체 처리)
  fetch(url).then((response) => {
    response.json().then((json) => {
      // 삭제된 task가 반영되 전체 tast 목록 자져오기 함수 호출
      get_todo_list()

    })
  })
}
</script>

<main>
  <form action="" method="">
    <textarea bind:value={task} name="task" rows="5" placeholder="Enter your task" id="task" required></textarea>
    {#if task_edit==true}
      <label for="completed">Done?</label>
      {#if _todo.completed} 
        <!-- _todo.completed가 1일때 -->
        <input bind:value={completed}  type="checkbox" name="completed" checked>
      {:else}    
        <!-- _todo.completed가 0일때 -->
        <input  bind:value={completed}  type="checkbox" name="completed">
      {/if}
      <button type="submit" id="add_task" 
        on:click={(event)=>update_edit_todo(event, _todo.id)}>
        Edit
      </button>
    {:else}  
      <!-- 입력 상태 일때 -->
      <button type="submit" id="add_task" on:click={add_todo}>
        Add
      </button>
    {/if}
  </form>

  <br>
  <h2>Tasks</h2>

  <div>
    {#if todos == 0 }
      <br>
      <p> 입력한 TODO 메모가 없습니다. </p>
    {:else}
      {#each todos as todo}
      <div class="task">
          {#if todo.completed}
              <strike>{todo.task}</strike>
          {:else}
              {todo.task}
          {/if}
          <small>
              <a href="/edit/{todo.id}" on:click={(event) => get_edit_todo(event, todo.id)} >Edit</a>
              <a href="/delete/{todo.id}" on:click={(event) => delete_todo(event, todo.id)}>Delete</a>
          </small>
      </div>
      {/each}
    {/if}
  </div>
</main>
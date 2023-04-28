const myTodos = document.getElementById('myTodos');

const updateTodo = async (id, checked) => {
  const todoId = parseInt(id);
  if (!Number.isInteger(todoId)) {
    return;
  }
  const url = `/todo/${todoId}`;
  const body = JSON.stringify({ done: !!checked });
  const headers = { 'Content-Type': 'application/json' };

  const res = await fetch(url, { method: 'PUT', body, headers });
  if (!res.ok) return;

  return true;
};

if (myTodos) {
  const checkBoxes = document.querySelectorAll(
    "table[id='myTodos'] td input[type='checkbox']"
  );
  checkBoxes.forEach((checkBox) => {
    checkBox.onchange = async () => {
      checkBox.disabled = true;
      const todoId = checkBox.getAttribute('record-id');
      const { checked } = checkBox;

      const done = await updateTodo(todoId, checked);
      if (!done) {
        alert('Something went wrong when updating todo');
        checkBox.disabled = false;
        return;
      }

      const todoText = checkBox.parentElement.parentElement.children[1];
      if (checked) todoText.classList.add('line-through');
      else todoText.classList.remove('line-through');
      checkBox.disabled = false;
    };
  });
}

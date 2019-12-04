const fetch = require('node-fetch');

let user = {
     key1: '11111', key2: '22222', key3: '33333' 
  };

const url = 'http://127.0.0.1:5000/api/single';

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(user)
})
.then(response => response.json()) // преобразуем ответ в json
.then(data => {
  console.log(data) // выводим в консоль результат выполнения response.json()
})
.catch(error => console.error(error));



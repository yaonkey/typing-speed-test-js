/*
* скрипт вызывается перед стартом
* основного функционала приложения
*/
// библиотеки
const fs = require('fs');

// имя файла с сохранением результатов
const FILENAME = '.typing-speed-test.results.json';

window.addEventListener('DOMContentLoaded', () => {
  // создание пустого файла в рабочей директории
  try {
    if (!fs.existsSync(FILENAME)){
      fs.writeFile(FILENAME, '', function(){
        console.log('Creating save-file...');
      }); 
    }
  } catch (err) {
    console.log(err);
  }
  
  
  // определение селекторов в программе
  const replaceText = (selector, text) => {
    const element = document.getElementById(selector)
    if (element) element.innerText = text
  }
});

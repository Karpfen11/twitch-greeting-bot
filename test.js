function func(ms) {
  var start = new Date().getTime();
  var end = 0
  while((end-start) < ms) {
    end = new Date().getTime();
    //hier kann was in der zeit ausgeführt werden
  }
}

console.log(func(1000));

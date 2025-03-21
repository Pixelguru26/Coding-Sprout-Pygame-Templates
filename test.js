(() => {
  let print = console.log;
  let isNumber = (n) => { return !isNaN(parseFloat(n)) && !isNaN(n - 0) }
  let lerp = (v, a = 0, b = 1) => {
    return v * (b - a) + a;
  }
  let wrap = (v, a = 0, b = 1) => {
    if (v < a) {
      let diff = a - v - 1;
      diff = diff % (b - a);
      return b - diff - 1;
    }
    return ((v - a) % (b - a)) + a;
  }

  print("Test successful");

})();
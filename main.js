(async () => {
  let pyodide = await loadPyodide();
  // Convenience function for transferring a py file alone
  // Note that it still needs to be loaded
  async function fetchText(src) {
    const libpackage = await fetch(src+".py");
    const bin = await libpackage.text();
    pyodide.FS.writeFile("/home/pyodide/"+src+".py", bin);
    return bin;
  }
  // Loading the core zip moved to a separate function for clarity
  async function fetchzip(src) {
    const zippackage = await fetch(src+".zip");
    const bin = await zippackage.arrayBuffer();
    pyodide.unpackArchive(bin, "zip", {extractDir: "/home/pyodide/"+src});
  }

  let canvas = tabs.shadowRoot.getElementById("game-canvas");
  let canvctx = canvas.getContext("2d");
  canvas.width = 900;
  canvas.height = 600;

  const pathMain = "/home/pyodide/main.py";
  var usrstore = window.localStorage;
  let usrtext = usrstore.getItem("main");
  if (usrtext) {
    pyodide.FS.writeFile(pathMain, usrtext);
  } else {
    // usrtext = usrstore.getItem("main") ?? await fetchText("main");
    usrtext = usrstore.getItem("main") ?? defaultpy;
  }

  // ==========================================
  // Console
  // ==========================================
  printin = (txt) => {
    consoleMain.session.insert({
      row: consoleMain.session.getLength(),
      column: 0
    }, txt.toString());
    consoleMain.scrollToLine(consoleMain.session.getLength());
  }
  /**
   * @param {string} txt 
   */
  print = (txt) => {
    printin(txt + "\n");
  }

  let consoleQue = [];
  let consoleInput = tabs.shadowRoot.getElementById("console-input");
  if (consoleInput) {
    consoleInput.onkeydown = (evt) => {
      if (evt.key === "Enter") {
        let text = consoleInput.value;
        consoleInput.value = '';
        consoleQue.push(text);
        print(text);
        jslib.usrgame?.command?.(text);
      }
    }
  }

  // ==========================================
  // Editor
  // ==========================================

  let saveMain = async (force = false) => {
    let v = editor.getValue();
    pyodide.FS.writeFile(pathMain, v);
    if (usrtext == v && !force) return v;
    usrtext = v;
    usrstore.setItem("main", v);
    // editorToggleButton.style.color = "#272822";
    reloadIcon.classList.add("active");
    unsavedIcon.classList.remove("active");
    return v;
  }
  /**
   * Loads stored data into the text editor and updates the usergame script from it.
   */
  let loadMain = async () => {
    usrtext = usrstore.getItem("main");
    if (usrtext && usrtext !== "") {
      editor.setValue(usrtext);
      pyodide.FS.writeFile(pathMain, usrtext);
      usrgame = pyodide.pyimport("main");
      jslib.usrgame = usrgame;
    } else {
      // editor.setValue(await fetchText("main"));
      editor.setValue(defaultpy);
    }
  }

  editor.addEventListener("change", (delta) => {
    // editorToggleButton.style.color = "lightgray";
    unsavedIcon.classList.add("active");
  });
  let editorInit = async (editor, usrtext) => {
    editor.setValue(usrtext, -1);
    // editorToggleButton.style.backgroundColor = "#757770"; // Remove gray-out of toggle
    // editorToggleButton.style.color = "#272822"; // Undo the unsaved indication from setting the initial text
    unsavedIcon.classList.remove("active"); // Undo the unsaved indication from setting the initial text
  }
  let doctimer = 0;
  let allowSave = true;
  let updateDoc = (dt) => {
    if (allowSave)
      doctimer += dt;
    if (doctimer > 20) {
      doctimer = 0;
      allowSave = false;
      saveMain().then(() => {allowSave = true;});
    }
  }
  editorInit(editor, usrtext);

  // ==========================================
  // Reload button
  // ==========================================

  let anim = reloadIcon.animate([
    { transform: "rotate(0deg)" },
    { transform: "rotate(360deg)" }
    ], {
      duration: 2000,
      easing: "linear",
      iterations: Infinity
    }
  );
  anim.pause();
  reloadIcon.onmouseover = (evt) => {
    anim.play();
  }
  reloadIcon.onmouseout = (evt) => {
    anim.pause();
  }
  
  // ==========================================
  // Canvas
  // ==========================================
  
  canvas.onmousedown = function(evt) {
    let boundrect = canvas.getBoundingClientRect();
    if (game?.running) {
      game.mousedown(evt.button, evt.x - boundrect.left, evt.y - boundrect.top);
      jslib.usrgame.mousedown?.(evt.button, evt.x, evt.y);
    }
  }
  canvas.onmouseup = function(evt) {
    let boundrect = canvas.getBoundingClientRect();
    if (game?.running) {
      game.mouseup(evt.button, evt.x - boundrect.left, evt.y - boundrect.top);
      jslib.usrgame.mouseup?.(evt.button, evt.x, evt.y);
    }
  }
  document.body.onkeydown = function(evt) {
    if (game?.running) {
      game.keydown(evt);
      jslib.usrgame.keydown?.(evt.key);
    }
    if (evt.ctrlKey && evt.key === 's') {
      // Prevent the Save dialog from opening
      evt.preventDefault();
      saveMain(true);
    }
  }
  document.body.onkeyup = function(evt) {
    if (game?.running) {
      game.keyup(evt);
      jslib.usrgame.keyup?.(evt.key);
    }
  }
  
  // ==========================================
  // Game
  // ==========================================

  function pycall(fn, ...params) {
    let ret;
    try {
      ret = fn(...params);
    } catch (e) {
      console.log(e);
    }
    return ret;
  }

  function pyload(id) {
    let ret;
    try {
      ret = pyodide.pyimport(id);
      return ret;
    } catch (e) {
      let msg = e.message;
      if (e instanceof pyodide._api.PythonError) {
        let i = e.message.indexOf("File");
        i += "File".length;
        i = e.message.indexOf("File", i);
        if (i > 0 && i < e.message.length)
          msg = e.message.slice(i);
      }
      msg = `Err [${(new Date()).toLocaleTimeString()}]:\t${msg}`;
      console.log(msg);
      print(msg);
    }
    return {};
  }
  
  async function gameInit() {
    gameData.build();
    game.graphics.init(canvctx);
    pyodide.registerJsModule("game", game);
    pyodide.setStderr({batched: (err) => {print(err);}});
    pyodide.setStdout({batched: (txt) => {print(txt);}});
    await saveMain();
    let usrgame = pyload("main");
    
    await game.load(usrgame, tabs.shadowRoot.getElementById("game-ui-layer"));
    usrgame.load?.();
    game.running = true;
  }
  async function reloadGame() {
    game.running = false;
    tabs.shadowRoot.getElementById("game-ui-layer").textContent = '';
    canvctx.reset();
    pyodide = await loadPyodide();
    reloadIcon.classList.remove("active");
    await gameInit();
  }
  
  await gameInit();
  
  reloadIcon.onclick = reloadGame;

  // ==========================================
  // Execution
  // ==========================================

  // Core event loop
  let last_time = Date.now();
  let dt, current_time;
  while (true) {
    current_time = Date.now();
    dt = (current_time - last_time)/1000; // Convert from ms => s
    last_time = current_time;

    // Flush at beginning and end to minimize unloaded assets
    if (game?.running) {
      await game.Asset.flush();
      await game.update(dt);
      jslib.usrgame?.update?.(dt, game.Asset);
      await game.Asset.flush();

      await game.draw(canvctx);
      jslib.usrgame?.draw?.(canvctx);
    }

    updateDoc(dt);

    await new Promise(r => setTimeout(r, 1));
  };
})();

var JSECore = class {
  static mousemove(evt) {

  }
  static mouseup(evt) {

  }
  static mousedown(evt) {

  }
  /**
   * 
   * @param {MouseEvent} evt 
   */
  static mouseEvent(evt) {
    switch (evt.type) {
      case "mousemove":
        this.mousemove(evt);
        break;
      case "mouseup":
        this.mouseup(evt);
        break;
      case "mousedown":
        this.mousedown(evt);
        break;
    }
  }
};

class JSEBase extends HTMLElement {
  constructor() {
    super();
  }
}

class JSETab extends HTMLElement {
  constructor() {
    super();
    this.onclick = this.inst_onclick;
    this.onpointerdown = this.enabledrag;
    this.onpointermove = this.begindrag;
    this.pointerdrag = this.pointerdrag.bind(this);
    this.enddrag = this.enddrag.bind(this);
    this.dummy = jslib.buildElement("span", null, {
      display: "inline-block"
    });
    this.dummy.classList.add("jse-tab-dummy");
  }
  pressed = false;
  posx = 0;
  posy = 0;
  enabledrag(evt) {
    this.dragenabled = true;
  }
  /**
   * @param {PointerEvent} evt 
   */
  pointerdrag(evt) {
    if (evt.buttons & 1) {
      if (evt.type === "pointermove") {
        this.posx += evt.movementX;
        this.style.left = `${this.posx}px`;
      }
    } else {
      this.enddrag();
    }
  }
  begindrag(evt) {
    if ((evt.buttons & 1) && this.dragenabled) {
      this.dragenabled = false;
      this.posx = this.offsetLeft;
      this.style.position = "absolute";
      this.style.opacity = "50%";
      document.addEventListener("pointermove", this.pointerdrag, { passive: true });
      document.addEventListener("pointerup", this.enddrag, { passive: true });
      let bounds = this.getBoundingClientRect();
      this.dummy.width = bounds.width;
      this.dummy.height = bounds.height;
      this.insertAdjacentElement("beforebegin", this.dummy);
    }
  }
  enddrag() {
    this.dummy.remove();
    this.style.removeProperty("position");
    this.style.removeProperty("opacity");
    this.style.removeProperty("offset-position");
    this.posx = 0;
  }
  inst_onclick(evt) {
    this.pane.setTab(this);
  }
  activate() {
    this.classList.add("active");
  }
  deactivate() {
    this.classList.remove("active");
  }
  connectedCallback() {
    this.classList.add("prevent-select");
  }
}
// customElements.define("jse-tab", JSETab);

class JSENewTabbedPanel extends HTMLElement {
  static __id = 0;

  tabs = [];
  lastTab = null;
  
  constructor() {
    super();
    this.attachShadow({mode: "open"});
    this.shadowRoot.append(jslib.buildElement("script", {
      src: "https://cdnjs.cloudflare.com/ajax/libs/ace/1.37.1/ace.js",
      integrity: "sha512-qLBIClcHlfxpnqKe1lEJQGuilUZMD+Emm/OVMPgAmU2+o3+R5W7Tq2Ov28AZqWqZL8Jjf0pJHQZbxK9B9xMusA==",
      crossorigin: "anonymous", referrerpolicy: "no-referrer"
    }));
    this.shadowRoot.append(jslib.buildElement("link", {
      rel: "stylesheet",
      type: "text/css",
      href: "./JSEStyles/JSETabContainer.css",
    }));
    this.navbar = jslib.buildElement("nav");
    this.shadowRoot.append(this.navbar);
    this.body = jslib.buildElement("main");
    this.shadowRoot.append(this.body);
    this.__id = JSENewTabbedPanel.__id++;
  }

  connectedCallback() {
    jslib.setCSS(this, {
      width: "100%",
      height: "100%",
      position: "relative",
      display: "flex",
      flexDirection: "column",
      borderRadius: "4px",
      overflow: "hidden",
      border: "2px solid #122"
    });
    this.observer = new MutationObserver((changes) => {
      for (let change of changes) {
        if (change.target === this) {
          this.onChanged(change);
        }
      }
    });
    this.observer.observe(this, {childList: true});
  }

  /**
   * @param {MutationRecord} change 
   */
  onChanged(change) {
    for (let node of change.addedNodes) {
      if (node.nodeType !== 3) {
        this.removeChild(node);
        this.addTab(node);
        for (let tgt of node.childNodes) {
          if (tgt.nodeType === Node.ELEMENT_NODE && tgt.classList.contains("plsedit")) {
            let temp = tgt;
            if (temp) {
              temp = ace.edit(temp, {
                  theme: "ace/theme/monokai",
                  mode: "ace/mode/python",
                  autoScrollEditorIntoView: true
                }
              );
              temp.renderer.attachToShadowRoot();
            }
          }
        }
      }
    }
  }

  static tab = class Tab {
    /**
     * @param {HTMLElement} content 
     */
    constructor(parent, content, title = null) {
      this.parent = parent;
      // Sequential priorities for possible titles
      title ||= (content.title != "") && content.title;
      title ||= (content.id != "") && content.id?.capitalize();
      title ||= "New Tab"; // Default if no others specified
      this.title = title;

      this.label = jslib.buildElement("div", {
        class: "jse-tab prevent-select",
        textContent: title
      });
      this.label.tabParent = this;
      this.content = content;
      this.__content_original_display = content.style.display;
      content.style.display = "none";
      this.label.onclick = function(evt) {
        this.tabParent.parent.setTab(this.tabParent);
      }
    }

    set contentVisible(v) {
      this.content.style.display = v ? this.__content_original_display : "none";
    }
    get contentVisible() {
      return this.content.style.display !== "none";
    }

    toggleContentVisible() {
      this.contentVisible = !this.contentVisible;
    }

    activate() {
      this.contentVisible = true;
      this.label.classList.add("active");
    }
    deactivate() {
      this.contentVisible = false;
      this.label.classList.remove("active");
    }
  }

  addTab(content, title = null) {
    let tab = new JSENewTabbedPanel.tab(this, content, title);
    this.tabs.push(tab);
    this.navbar.append(tab.label);
    this.body.append(tab.content);
    if (this.tabs.length < 2) {
      this.setTab(tab);
    }
    return tab;
  }
  setTab(tab) {
    tab = this.tabs[tab] || tab;
    if (tab instanceof JSENewTabbedPanel.tab) {
      this.lastTab?.deactivate();
      tab.activate();
      this.lastTab = tab;
      return tab;
    }
  }
}
customElements.define("jse-tab", JSENewTabbedPanel.tab);
customElements.define("jse-new-tabbed-panel", JSENewTabbedPanel);

// class JSETabbedPanel extends HTMLElement {
//   constructor() {
//     super();
//     this.attachShadow({mode: "open"});
//     this.shadowRoot.append(jslib.buildElement("link", {
//       rel: "stylesheet",
//       type: "text/css",
//       href: "./JSEStyles/JSETabContainer.css"
//     }));
//     this.navbar = jslib.buildElement("nav");
//     this.shadowRoot.append(this.navbar);
//     this.body = jslib.buildElement("main");
//     this.shadowRoot.append(this.body);
//     this.tabs = [];
//   }

//   lastTab = null;
//   setTab(tab) {
//     if (tab !== this.lastTab) {
//       this.lastTab?.deactivate();
//       this.body.replaceChildren();
//       this.body.append(tab.tabContent);
//       tab.activate();
//       this.lastTab = tab;
//     }
//   }

//   connectedCallback() {
//     // Styling here
//     jslib.setCSS(this, {
//       width: "100%",
//       height: "100%",
//       position: "relative",
//       display: "flex",
//       flexDirection: "column",
//       borderRadius: "4px",
//       overflow: "hidden",
//       border: "2px solid #122"
//     });
//     this.observer = new MutationObserver((changes, observer) => {
//       for (let change of changes) {
//         if (change.target === this) {
//           this.onChanged(change);
//         }
//       }
//     });
//     this.observer.observe(this, {childList: true});
//   }

//   /**
//    * @param {string} str 
//    */
//   static capitalize(str) {
//     return str.replace(/\b\w/g, (c) => c.toUpperCase());
//   }

//   /**
//    * @param {HTMLElement} content 
//    */
//   addTab(content) {
//     let ret = jslib.buildElement("jse-tab", {
//       textContent: (content.title && content.title != "") ? content.title : (content.id && content.id != "") ? JSETabbedPanel.capitalize(content.id) : "new tab"
//     });
//     ret.tabContent = content;
//     ret.pane = this;
//     this.navbar.append(ret);
//     this.tabs.push(ret);
//   }

//   /**
//    * @param {MutationRecord} change 
//    */
//   onChanged(change) {
//     for (let node of change.addedNodes) {
//       if (node.nodeType !== 3) {
//         this.removeChild(node);
//         this.addTab(node);
//       }
//     }
//   }
// }
// customElements.define("jse-tabbed-panel", JSETabbedPanel);

// ==========================================


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

class JSENewTabbedPanel extends HTMLElement {
  static __id = 0;

  tabs = [];
  lastTab = null;
  
  constructor() {
    super();
    this.attachShadow({mode: "open"});
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
      if (node.nodeType === Node.ELEMENT_NODE) {
        this.removeChild(node);
        if (["STYLE", "SCRIPT", "LINK"].includes(node.tagName)) {
          this.shadowRoot.prepend(node);
        } else {
          this.addTab(node);
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
        textContent: title,
        style: {
          position: "relative"
        }
      });
      let tooltip;
      for (const element of content.children) {
        if (element.tagName === "SUMMARY") {
          tooltip = element;
          break;
        }
      }
      if (tooltip) {
        tooltip.remove();
        this.tooltip = jslib.buildElement("div", {
          class: "jse-tab-tooltip",
          style: {
            position: "absolute"
          }
        });
        this.tooltip.append(tooltip);
        this.label.append(this.tooltip);
      }
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


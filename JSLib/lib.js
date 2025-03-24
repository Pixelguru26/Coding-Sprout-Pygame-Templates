class JSLib2 {
  static isString(v) {
    return (typeof v === 'string' || v instanceof String) ? v : null;
  }
  /**
   * "is Valid String"\
   * Returns v if it is a valid, non-empty string.
   * @param {*} v 
   * @returns {string | null} v
   */
  static isVString(v) {
    v = JSLib2.isString(v);
    return (v != "") ? v : null;
  }
  /**
   * 
   * @param {HTMLElement} obj 
   * @param {string|CSSStyleDeclaration} style Either a string containing inline style attributes, or a map of properties
   * @returns {HTMLElement}
   */
  static style(obj, style) {
    if (JSLib2.isString(style)) {
      obj.style.cssText += style;
    } else {
      let t = obj.style;
      for (let k in style) {
        t[k] = style[k];
      }
    }
    return obj;
  }
  /** Identifies events to handle them non-destructively. */
  static HTMLEvents = {}
  /** Aliases for certain properties to make attributes more intuitive. */
  static HTMLAliases = {}
  /**
   * Sets many attributes of an element at once from a mapping table.\
   * Includes special casing for many attributes, including style, content, and events.
   * Largely internal, build() is usually preferable.
   * @param {HTMLElement} obj The target element whose attributes will be assigned to
   * @param {HTMLElement} data A table of element properties to be assigned
   * @returns {HTMLElement}
   */
  static attr(obj, data) {
    if (!data) return obj;
    let lowerk, altk, evtk, v;
    for (let k in data) {
      v = data[k];
      lowerk = k.toLowerCase();
      switch (lowerk) {
        case "style":
          JSLib2.style(obj, v);
          break;
        case "innerHTML":
        case "textContent":
          obj[k] = data[v];
          break;
        case "class": // Included to indicate that it doesn't work otherwise
        default:
          altk = JSLib2.HTMLAliases[lowerk];
          evtk = JSLib2.HTMLEvents[altk ?? lowerk];
          if (evtk) {
            // Events are added instead of replaced where possible
            obj.addEventListener(evtk, v);
          } else if (typeof v === "function") {
            obj[k] = v;
          } else {
            // Normal attribute (probably)
            obj.setAttribute(altk ?? k, v);
          }
          break;
      }
    }
    return obj;
  }
  /**
   * Creates an element (if necessary) and sets many attributes at once from a mapping table.\
   * Includes special casing for many attributes, including style, content, and events.
   * @param {string|HTMLElement} tag Either a string indicating the tag to construct an element from, or the element itself.
   * @param {HTMLElement} data A table of element properties to be assigned
   * @returns {HTMLElement}
   */
  static build(tag, data) {
    if (JSLib2.isString(tag)) {
      tag = document.createElement(tag);
    }
    return JSLib2.attr(tag, data);
  }
  static buildTree(data, parent, reference) {
    if (!data) return;
    // Build simple text node when passed a string
    if (JSLib2.isVString(data)) {
      let t = document.createTextNode(data);
      if (parent) parent.appendChild(t);
      return t;
    }
    // Weird case for simple appending
    if (data instanceof Node && parent instanceof Node) {
      parent.appendChild(data);
      return data;
    }
    // Case for many elements (used in recursion)
    if (!JSLib2.isString(data[0])) {
      let ret = [];
      for (let element of data)
        ret.push(JSLib2.buildTree(element, parent, reference));
      return ret;
    }
    // Main construction case
    let element;
    let start = 1;
    if (!(data[1] instanceof Node))
      element = JSLib2.build(data[0], data[start++]);
    else
      element = document.createElement(data[0]);
    for (let i = start; i < data.length; i++) {
      this.buildTree(data[i], element, reference);
    }
    if (parent) parent.appendChild(element);
    return element;
  }
}

// Add aliases for events
(() => {
  let evts = `
    cancel change error load copy cut paste drag
    dragend dragenter dragleave dragover dragstart
    drop beforetoggle toggle
    afterscriptexecute beforeinput beforematch
    beforescriptexecute beforexrselect
    contentvisibilityautostatechange
    input securitypolicyviolation wheel
    animationcancel animationend animationiteration
    animationstart
    compositionend compositionstart compositionupdate
    blur focus focusin focusout
    fullscreenchange fullscreenerror
    keydown keypress keyup
    auxclick click contextmenu dblclick domactivate
    dommousescroll
    mousedown mouseenter mouseleave mousemove
    mouseout mouseover mouseup
    gotpointercapture lostpointercapture
    pointercancel pointerdown pointerenter
    pointerleave pointermove pointerout
    pointerover pointerrawupdate pointerup
    scroll scrollend
    touchcancel touchend touchmove touchstart
    transitioncancel transitionend transitionrun
    transitionstart
  `.split(/[\s\,]+/g);
  for (let evt in evts) {
    JSLib2.HTMLAliases["on"+evt] = evt;
    JSLib2.HTMLEvents[evt] = evt;
    JSLib2.HTMLEvents["on"+evt] = evt;
  }
})();
gameData.libs.push(() => {
  let ui = game.ui = class UI {
    static element = class UIElement {
      /**
       * Will mark the wrapped element with a "parentUIElement" property pointing to this object.
       * @param {Element | String} element Root element used whenever this ui element is embedded into an HTML element
       * @param {{}?} properties HTML properties map which will be applied to the element if provided.
       * @param {{}?} css CSS properties map which will be applied to the element if provided.
       */
      constructor(element, properties = null, css = null) {
        if (jslib.isString(element)) {
          this.element = jslib.newElement(element, properties, css);
        } else {
          /** @type {Element} */
          this.element = element;
        }
        this.element.parentUIElement = this;
      }

      /**
       * Adds an element to this UIElement's wrapped HTML element.
       * @param {UIElement | Element | string} element Element or or tag to be added. If a tag, a new Element will be created and returned.
       * @param {{}?} properties Optional property map which will be applied to the HTML element
       * @param {{}?} css Optional property map which will be applied as the styling fo the HTML element
       * @returns {UIElement | Element}
       */
      addElement(element, properties = null, css = null) {
        if (element instanceof UIElement) {
          // I'm sorry for this awful line
          this.element.append(jslib.setProps(element.element));
        } else if (jslib.isString(element)) {
          // Element must be created before insertion
          element = jslib.newElement(element, properties, css);
          this.element.append(element);
        } else {
          // Assumes normal element
          this.element.append(jslib.setProps(element, properties, css));
        }
        return element;
      }
    }

    /**
     * A custom UI element designed to display a value out of its maximum in a visually pleasing way.
     */
    static circleDisplay = class CircleDisplay extends UI.element {
      /**
       * @param {Number} value Initial display value, also used to calculate circular indicator.
       * @param {Number} maxValue Secondary display value, also used to calculate circular indicator.
       * @param {Number} width Width in pixels
       * @param {Number?} height Height in pixels, otherwise same as width. Rarely any reason to change this.
       */
      constructor(value, maxValue, width, height = null) {
        super("div", null, {
          display: "inline-block",
          position: "absolute"
        });
        this.width = width;
        this.height = height ?? width;

        this.svg = jslib.appendNewSVG(this.element, "svg", {
          class: "circular-progress"
        });
        this.circle = jslib.appendNewSVG(this.svg, "circle", {
          class: "fg",
          style: {
            transition: "stroke-dasharray 0s linear",
            cx: `${this.width / 2}px`, // Center x
            cy: `${this.height / 2}px`, // Center y
            r: `${Math.min(this.width, this.height) / 2 - 10}px`, // Radius
            strokeWidth: "4px",
            stroke: "white",
            fill: "none"
          }
        });
        this.content = jslib.appendElement(this.element, "div", null, {
          position: "absolute",
          isolation: "isolate",
          padding: 0,
          top: 0, bottom: 0, left: 0, right: 0,
          width: "fit-content", height: "fit-content",
          margin: "auto"
        });
        this.displayText1 = jslib.appendElement(this.content, "p", null, {
          color: "white",
          align: "center",
          textAlign: "center",
          margin: 0
        });
        this.bar = appendElement(this.content, "hr", null, {
          borderTop: "3px solid white"
        });
        this.displayText2 = jslib.appendElement(this.content, "p", null, {
          color: "white",
          align: "center",
          textAlign: "center",
          margin: 0
        });

        this.maxValue = maxValue;
        this.value = value;
      }

      updateDims() {
        jslib.setCSS(this.element, {
          left: `${this.x}px`,
          top: `${this.y}px`
        });
        jslib.setProps(this.svg, {
          viewbox: `0, 0, ${this.width}, ${this.height}`,
          width: this.width,
          height: this.height
        });
        this.svg.style.setProperty("--total-radius", `${Math.min(this.width, this.height) / 2}px`);
      }

      get text() { return this.displayText1.textContent + "/" + this.displayText2.textContent; }
      /** Assigned value should be in the format "top/bottom". It will be split at the slash. */
      set text(v) {
        let [top, bottom] = v.split("/");
        top = top.trim();
        bottom = bottom.trim();
        this.displayText1.textContent = top;
        this.displayText2.textContent = bottom;
      }

      get value() { return this.__value; }
      set value(v) {
        this.__value = v;
        this.displayText1.textContent = v;
        this.displayText2.textContent = this.maxValue;
        this.svg.style.setProperty("--progress", v / this.maxValue);
      }
    }

    static universalStyle = document.createElement("style");

    static circleDisplayAlt = class CircleDisplayAlt extends UI.element {
      constructor(value, maxValue, width, height = null) {
        super(jslib.newSVG("svg", { class: "circular-progress" }));
        this.width = width;
        this.height = height ?? width;
        this.textElement = jslib.newSVG("text", { fill: "white" });
        this.text = "0/0";
        this.element.append(this.textElement);
        this.circle = jslib.newSVG("circle", { class: "fg" });

        this.__value = new game.util.smoothVal(value, 0, maxValue);
        this.updateDims();
      }

      static __ = UI.universalStyle.innerHTML += CircleDisplayAlt.style;

      updateDims() {
        jslib.setProps(this.element, {
          width: this.width,
          height: this.height,
          viewbox: `0, 0, ${this.width}, ${this.height}`
        });
        this.element.style.setProperty("--total-radius", `${Math.min(this.width, this.height) / 2}px`);
        let textBox = this.textElement.getBBox();
        let textWidth = textBox.width;
        let textHeight = textBox.height;
        this.textElement.setAttribute("x", (this.width - textWidth) / 2);
        this.textElement.setAttribute("y", (this.height + textHeight) / 2);
      }

      get text() { return this.textElement.textContent; }
      set text(v) {
        this.textElement.textContent = v;
        this.updateDims();
      }

      get value() { return this.__value.val; }
      set value(v) {
        this.__value.val = v;
      }
    }

    /**
     * An element designed to display health, armor, shields, etc. in a layered
     * and multicolored bar. Using gradient layers, they can change color
     * depending on their level - for example, green when full, red when empty.
     */
    static barDisplay = class BarDisplay extends UI.element {
      constructor(width, height, ...layers) {
        super("div", null, {
          width: width + "px",
          height: height + "px"
        });
        this.layers = layers;
        this.width = width;
        this.height = height;
      }

      addLayer(v) {
        v.parent = this;
        if (this.layers.last) {
          jslib.appendElement(this.layers.last.bar, v.backBar);
        } else {
          jslib.appendElement(this.element, v.backBar);
        }
        this.layers.push(v);
      }

      static layer = class Layer {
        constructor(parent, max, foreground = "red", background = "darkred", shine = true) {
          this.parent = parent;
          this.tracker = new game.util.smoothVal(max, 0, max);
          this.foreground = foreground;
          this.background = background;
          this.backBar = jslib.newElement("div", null, {
            width: "0px",
            height: "inherit"
          });
          this.bar = jslib.appendElement(this.backBar, "div", null, {
            width: "0px",
            height: "inherit"
          });
          this.shine = shine;
          this.__lastUpdatedValue = 0;
        }

        set value(v) {
          if (v === this.tracker.val) return;
          this.tracker.val = v;
          this.bar.style.width = (v / this.tracker.max * this.parent.width) + "px";
          this.updateStyle();
        }
        get value() { return this.tracker.val; }

        get foreground() { return this.__foreground; }
        set foreground(v) { this.__foreground = v; }
        get background() { return this.__background; }
        set background(v) { this.__background = v; }

        /**
         * 
         * @param {string | [h, s, l, a] | [r, g, b, a]} color
         * @param {Boolean?} colorIsHSLA Set to false if color is in [r, g, b, a] format
         * @returns 
         */
        static generateShineCSS(color, colorIsHSLA = true) {
          let light = color;
          // Mutate "light" into the lighter color to use for shine
          // Convert color to hsla first
          if (!Array.isArray(light)) {
            light = game.util.csstorgb(color);
            light = game.util.rgbtohsl(...light);
          } else {
            if (!colorIsHSLA) light = game.util.rgbtohsl(...light);
          }
          // Increase lightness
          light[2] = Math.min(100, light[2] + 20);
          // Convert to useable css form
          light = game.util.cssColor(light);
          return `linear-gradient(180deg, 
          ${light},
          ${color} 10%,
          ${light} 50%,
          ${color} 50%,
          ${color} 90%,
          ${light}
        )`;
        }

        set shine(v) {
          this.__shine = !!v;
          this.updateStyle(true);
        }
        get shine() { return this.__shine; }

        updateStyle(force = false) {
          // Declared here to adapt returns
          let background = this.background;
          let foreground = this.foreground;
          // Update foreground
          if (force || (this.__lastUpdatedValue != this.tracker.val)) {
            if (this.__shine) {
              // Clear non-shiny styling
              this.bar.style.backgroundColor = null;
              // Generate gradient
              foreground = Layer.generateShineCSS(foreground);
              this.bar.style.backgroundImage = foreground;
            } else {
              this.bar.style.backgroundImage = null;
              this.bar.style.backgroundColor = foreground;
            }
          }
          // Update background
          if (force || (this.tracker.prevSmoothed != this.tracker.smoothVal)) {
            if (this.__shine) {
              // Clear non-shiny styling
              this.backBar.style.backgroundColor = null;
              // Generate gradient
              background = Layer.generateShineCSS(background);
              this.backBar.style.backgroundImage = background;
            } else {
              this.backBar.style.backgroundImage = null;
              this.backBar.backgroundColor = background;
            }
            // Return because why not
            return [background, foreground];
          }
        }

        update(dt) {
          if (this.tracker.prevSmoothed != this.tracker.smoothed) {
            this.backBar.style.width = (this.tracker.smoothed / this.tracker.max * this.parent.width) + "px";
            this.updateStyle();
          }
        }

      }
      static gradientLayer = class GradientLayer extends BarDisplay.layer {
        constructor(parent, max, foregroundGradient, backgroundGradient, shine = true) {
          super(parent, max, foregroundGradient, backgroundGradient, shine);
        }

        set foreground(v) { this.__foreground = v; }
        get foreground() {
          this.__foreground.caret = this.tracker.val;
          return this.__foreground.cssColor;
        }

        set background(v) { this.__background = v; }
        get background() {
          this.__background.caret = this.tracker.smoothed;
          return this.__background.cssColor;
        }
      }

      update(dt) {
        for (let i = 0; i < this.layers.length; i++) {
          this.layers[i].update(dt);
        }
      }
    }
  }
});
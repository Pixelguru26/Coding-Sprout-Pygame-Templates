/**
 * Type definition for html attributes used in construction functions.
 * @typedef {Element} HTMLAttributesMap
 * @description Vanilla javascript table containing attributes for an HTML element.
 * Properties
 * @property {string} accessKey
 * @property {string} accessKeyLabel (readonly)
 * @property {Element?} anchorElement (readonly)
 * @property {StylePropertyMap} attributeStyleMap (readonly)
 * @property {"none"|"off"|"on"|"characters"|"words"|"sentences"} autocapitalize
 * @property {boolean} autofocus
 * @property {boolean} autocorrect
 * @property {"true"|"false"} contentEditable
 * @property {DOMStringMap} dataset (readonly) used to read and write the element's custom data attributes (data-*).
 * @property {"ltr"|"rtl"|"auto"} dir
 * @property {boolean} draggable
 * @property {EditContext?} editContext
 * @property {boolean} inert indicates if the user agent must act as though the given node is absent for the purposes of user interaction events, in-page text searches ("find in page"), and text selection.
 * @property {string} innerText Represents the rendered text content of a node and its descendants. As a getter, it approximates the text the user would get if they highlighted the contents of the element with the cursor and then copied it to the clipboard. As a setter, it replaces the content inside the selected element, converting any line breaks into <br> elements
 * @property {"none"|"text"|"decimal"|"numeric"|"tel"|"search"|"email"|"url"} inputMode
 * @property {boolean} isContentEditable (readonly)
 * @property {string} lang
 * @property {number?} nonce Returns the cryptographic number that is used once by Content Security Policy to determine whether a given fetch will be allowed to proceed.
 * @property {number} offsetHeight (readonly) Returns a double containing the height of an element, relative to the layout.
 * @property {number} offsetLeft (readonly) Returns a double, the distance from this element's left border to its offsetParent's left border.
 * @property {Element} offsetParent (readonly) An Element that is the element from which all offset calculations are currently computed.
 * @property {number} offsetTop (readonly) Returns a double containing the distance from this element's top border to its offsetParent's top border.
 * @property {number} offsetWidth (readonly) Returns a double containing the width of an element, relative to the layout.
 * @property {string} outerText Represents the rendered text content of a node and its descendants. As a getter, it is the same as HTMLElement.innerText (it represents the rendered text content of an element and its descendants). As a setter, it replaces the selected node and its contents with the given value, converting any line breaks into <br> elements.
 * @property {"auto"|"hint"|"manual"} popover ets and sets an element's popover state via JavaScript ("auto", "hint", or "manual"), and can be used for feature detection. Reflects the value of the popover global HTML attribute.
 * @property {boolean} spellcheck A boolean value that controls the spell-checking hint. It is available on all HTML elements, though it doesn't affect all of them.
 * @property {CSSStyleDeclaration} style Represents the declarations of the element's style attribute.
 * @property {number} tabIndex A long representing the position of the element in the tabbing order.
 * @property {string} title A string containing the text that appears in a popup box when mouse is over the element.
 * @property {boolean} translate
 * @property {string} virtualKeyboardPolicy A string indicating the on-screen virtual keyboard behavior on devices such as tablets, mobile phones, or other devices where a hardware keyboard may not be available, if the element's content is editable (for example, it is an <input> or <textarea> element, or an element with the contenteditable attribute set).
 * @property {string} writingSuggestions A string indicating if browser-provided writing suggestions should be enabled under the scope of the element or not.
 * Methods
 * @property {function(): ElementInternals} attachInternals Returns an ElementInternals object, and enables a custom element to participate in HTML forms.
 * @property {function()} blur Removes keyboard focus from the currently focused element.
 * @property {function()} click Sends a mouse click event to the element.
 * @property {function()} focus Makes the element the current keyboard focus.
 * @property {function()} hidePopover Hides a popover element by removing it from the top layer and styling it with display: none.
 * @property {function()} showPopover Shows a popover element by adding it to the top layer and removing display: none; from its styles.
 * @property {function()} togglePopover Toggles a popover element between the hidden and showing states.
 * Events
 * @property {function(event: Event)} oncancel (event: cancel) Fired for <input> and <dialog> elements when the user cancels the currently open dialog by closing it with the Esc key.
 * @property {function(event: Event)} onchange (event: change) Fired when the value of an <input>, <select>, or <textarea> element has been changed and committed by the user. Unlike the input event, the change event is not necessarily fired for each alteration to an element's value.
 * @property {function(event: Event|UIEvent)} onerror (event: error) Fired when a resource failed to load, or can't be used.
 * @property {function(event: Event)} onload (event: load) Fires for elements containing a resource when the resource has successfully loaded.
 * Clipboard events
 * @property {function(event: ClipboardEvent)} oncopy (event: copy) Fired when the user initiates a copy action through the browser's user interface.
 * @property {function(event: ClipboardEvent)} oncut (event: cut) Fired when the user initiates a cut action through the browser's user interface.
 * @property {function(event: ClipboardEvent)} onpaste (event: paste) Fired when the user initiates a paste action through the browser's user interface.
 * Drag and drop events
 * @property {function(event: DragEvent)} ondrag (event: drag) This event is fired when an element or text selection is being dragged.
 * @property {function(event: DragEvent)} ondragend (event: dragend) This event is fired when a drag operation is being ended (by releasing a mouse button or hitting the escape key).
 * @property {function(event: DragEvent)} ondragenter (event: dragenter) This event is fired when a dragged element or text selection enters a valid drop target.
 * @property {function(event: DragEvent)} ondragleave (event: dragleave) This event is fired when a dragged element or text selection leaves a valid drop target.
 * @property {function(event: DragEvent)} ondragover (event: dragover) This event is fired continuously when an element or text selection is being dragged and the mouse pointer is over a valid drop target (every 50 ms WHEN mouse is not moving ELSE much faster between 5 ms (slow movement) and 1ms (fast movement) approximately. This firing pattern is different from mouseover.)
 * @property {function(event: DragEvent)} ondragstart (event: dragstart) This event is fired when the user starts dragging an element or text selection.
 * @property {function(event: DragEvent)} ondrop (event: drop) This event is fired when an element or text selection is dropped on a valid drop target.
 * Other
 * @property {function(event: ToggleEvent)} onbeforetoggle (event: beforetoggle) Fired when the element is a popover or <dialog>, before it is hidden or shown.
 * @property {function(event: ToggleEvent)} ontoggle (event: toggle) Fired when the element is a popover, <dialog>, or <details> element, just after it is hidden or shown.
 * 
 * Element events
 * @property {function(event: Event)} onafterscriptexecute (event: afterscriptexecute)
 * @property {function(event: Event)} afterscriptexecute (alias)
 * @property {function(event: Event)} onbeforeinput (event: beforeinput)
 * @property {function(event: Event)} beforeinput (alias)
 * @property {function(event: Event)} onbeforematch (event: beforematch)
 * @property {function(event: Event)} beforematch (alias)
 * @property {function(event: Event)} onbeforescriptexecute (event: beforescriptexecute)
 * @property {function(event: Event)} beforescriptexecute (alias)
 * @property {function(event: Event)} onbeforexrselect (event: beforexrselect)
 * @property {function(event: Event)} beforexrselect (alias)
 * @property {function(event: Event)} oncontentvisibilityautostatechange (event: contentvisibilityautostatechange)
 * @property {function(event: Event)} contentvisibilityautostatechange (alias)
 * @property {function(event: Event)} oninput (event: input)
 * @property {function(event: Event)} input (alias)
 * @property {function(event: Event)} onsecuritypolicyviolation (event: securitypolicyviolation)
 * @property {function(event: Event)} securitypolicyviolation (alias)
 * @property {function(event: Event)} onwheel (event: wheel)
 * @property {function(event: Event)} wheel (alias)
 * 
 * Animation events
 * @property {function(event: Event)} onanimationcancel (event: animationcancel)
 * @property {function(event: Event)} animationcancel (alias)
 * @property {function(event: Event)} onanimationend (event: animationend)
 * @property {function(event: Event)} animationend (alias)
 * @property {function(event: Event)} onanimationiteration (event: animationiteration)
 * @property {function(event: Event)} animationiteration (alias)
 * @property {function(event: Event)} onanimationstart (event: animationstart)
 * @property {function(event: Event)} animationstart (alias)
 * 
 * Composition events
 * @property {function(event: Event)} oncompositionend (event: compositionend)
 * @property {function(event: Event)} compositionend (alias)
 * @property {function(event: Event)} oncompositionstart (event: compositionstart)
 * @property {function(event: Event)} compositionstart (alias)
 * @property {function(event: Event)} oncompositionupdate (event: compositionupdate)
 * @property {function(event: Event)} compositionupdate (alias)
 * 
 * Additional focus events
 * @property {function(event: Event)} onfocusin (event: focusin)
 * @property {function(event: Event)} focusin (alias)
 * @property {function(event: Event)} onfocusout (event: focusout)
 * @property {function(event: Event)} focusout (alias)
 * 
 * @property {function(event: Event)} onfullscreenchange (event: fullscreenchange)
 * @property {function(event: Event)} fullscreenchange (alias)
 * @property {function(event: Event)} onfullscreenerror (event: fullscreenerror)
 * @property {function(event: Event)} fullscreenerror (alias)
 * 
 * @property {function(event: Event)} onkeydown (event: keydown)
 * @property {function(event: Event)} keydown (alias)
 * @property {function(event: Event)} onkeypress (event: keypress)
 * @property {function(event: Event)} keypress (alias)
 * @property {function(event: Event)} onkeyup (event: keyup)
 * @property {function(event: Event)} keyup (alias)
 * 
 * @property {function(event: Event)} onauxclick (event: auxclick)
 * @property {function(event: Event)} auxclick (alias)
 * @property {function(event: Event)} onclick (event: click)
 * @property {function(event: Event)} click (alias)
 * @property {function(event: Event)} oncontextmenu (event: contextmenu)
 * @property {function(event: Event)} contextmenu (alias)
 * @property {function(event: Event)} ondblclick (event: dblclick)
 * @property {function(event: Event)} dblclick (alias)
 * @property {function(event: Event)} onmousedown (event: mousedown)
 * @property {function(event: Event)} mousedown (alias)
 * @property {function(event: Event)} onmouseenter (event: mouseenter)
 * @property {function(event: Event)} mouseenter (alias)
 * @property {function(event: Event)} onmouseleave (event: mouseleave)
 * @property {function(event: Event)} mouseleave (alias)
 * @property {function(event: Event)} onmousemove (event: mousemove)
 * @property {function(event: Event)} mousemove (alias)
 * @property {function(event: Event)} onmouseout (event: mouseout)
 * @property {function(event: Event)} mouseout (alias)
 * @property {function(event: Event)} onmouseover (event: mouseover)
 * @property {function(event: Event)} mouseover (alias)
 * @property {function(event: Event)} onmouseup (event: mouseup)
 * @property {function(event: Event)} mouseup (alias)
 * 
 * @property {function(event: Event)} ongotpointercapture (event: gotpointercapture)
 * @property {function(event: Event)} gotpointercapture (alias)
 * @property {function(event: Event)} onlostpointercapture (event: lostpointercapture)
 * @property {function(event: Event)} lostpointercapture (alias)
 * @property {function(event: Event)} onpointercancel (event: pointercancel)
 * @property {function(event: Event)} pointercancel (alias)
 * @property {function(event: Event)} onpointerdown (event: pointerdown)
 * @property {function(event: Event)} pointerdown (alias)
 * @property {function(event: Event)} onpointerenter (event: pointerenter)
 * @property {function(event: Event)} pointerenter (alias)
 * @property {function(event: Event)} onpointerleave (event: pointerleave)
 * @property {function(event: Event)} pointerleave (alias)
 * @property {function(event: Event)} onpointermove (event: pointermove)
 * @property {function(event: Event)} pointermove (alias)
 * @property {function(event: Event)} onpointerout (event: pointerout)
 * @property {function(event: Event)} pointerout (alias)
 * @property {function(event: Event)} onpointerover (event: pointerover)
 * @property {function(event: Event)} pointerover (alias)
 * @property {function(event: Event)} onpointerrawupdate (event: pointerrawupdate)
 * @property {function(event: Event)} pointerrawupdate (alias)
 * @property {function(event: Event)} onpointerup (event: pointerup)
 * @property {function(event: Event)} pointerup (alias)
 * 
 * @property {function(event: Event)} onscroll (event: scroll)
 * @property {function(event: Event)} scroll (alias)
 * @property {function(event: Event)} onscrollend (event: scrollend)
 * @property {function(event: Event)} scrollend (alias)
 * 
 * @property {function(event: Event)} ontouchcancel (event: touchcancel)
 * @property {function(event: Event)} touchcancel (alias)
 * @property {function(event: Event)} ontouchend (event: touchend)
 * @property {function(event: Event)} touchend (alias)
 * @property {function(event: Event)} ontouchmove (event: touchmove)
 * @property {function(event: Event)} touchmove (alias)
 * @property {function(event: Event)} ontouchstart (event: touchstart)
 * @property {function(event: Event)} touchstart (alias)
 * 
 * @property {function(event: Event)} ontransitioncancel (event: transitioncancel)
 * @property {function(event: Event)} transitioncancel (alias)
 * @property {function(event: Event)} ontransitionend (event: transitionend)
 * @property {function(event: Event)} transitionend (alias)
 * @property {function(event: Event)} ontransitionrun (event: transitionrun)
 * @property {function(event: Event)} transitionrun (alias)
 * @property {function(event: Event)} ontransitionstart (event: transitionstart)
 * @property {function(event: Event)} transitionstart (alias)
 */
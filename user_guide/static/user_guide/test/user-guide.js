describe('DjangoUserGuide', function() {
    function appendDom(el) {
        document.body.appendChild(el);
    }

    function removeDom(el) {
        document.body.removeChild(el);
    }

    function createDom(html) {
        var el = document.createElement('div');
        el.innerHTML = html;
        return el;
    }

    function queryAllDom(selector) {
        return document.body.querySelectorAll(selector);
    }

    function getRenderedStyle(el, prop) {
        return getComputedStyle(el).getPropertyValue(prop);
    }

    it('should handle many items', function() {
        var dug = new window.DjangoUserGuide(),
            items = null,
            btns = null,
            cont = null,
            guide = createDom([
                '<div class="django-user-guide">',
                '   <div class="django-user-guide-mask">',
                '      <div class="django-user-guide-window">',
                '           <div class="django-user-guide-close-div">x</div>',
                '           <div class="django-user-guide-html-wrapper">',
                '               <div class="django-user-guide-item"><h1>MEGA GUIDE!!!</h1></div>',
                '               <div class="django-user-guide-item"><p>Hello guide 2</p></div>',
                '               <div class="django-user-guide-item"><p>Hello guide 1</p></div>',
                '           </div>',
                '           <div class="django-user-guide-window-nav">',
                '                <button class="django-user-guide-back-btn">&lt; Back</button>',
                '                <button class="django-user-guide-next-btn">Next &gt;</button>',
                '                <button class="django-user-guide-done-btn">Done</button>',
                '            </div>',
                '        </div>',
                '    </div>',
                '</div>'
            ].join('\n'));

        //add the guide to the dom
        appendDom(guide);

        //run the user guide
        dug.run();

        //examine the result
        items = queryAllDom('.django-user-guide-item');
        btns = queryAllDom('button');
        cont = queryAllDom('.django-user-guide');

        expect(getRenderedStyle(items[0], 'display')).toBe('block'); //should show the first item
        expect(getRenderedStyle(items[1], 'display')).toBe('none'); //should NOT show the second item
        expect(getRenderedStyle(items[2], 'display')).toBe('none'); //should NOT show the third item
        expect(getRenderedStyle(btns[0], 'display')).toBe('none'); //should NOT show the back button
        expect(getRenderedStyle(btns[1], 'display')).toBe('inline-block'); //should show the next button
        expect(getRenderedStyle(btns[2], 'display')).toBe('none'); //should NOT show the done button

        //click the next button
        dug.onNextClick();

        expect(getRenderedStyle(items[0], 'display')).toBe('none'); //should NOT show the first item
        expect(getRenderedStyle(items[1], 'display')).toBe('block'); //should show the second item
        expect(getRenderedStyle(items[2], 'display')).toBe('none'); //should NOT show the third item
        expect(getRenderedStyle(btns[0], 'display')).toBe('inline-block'); //should show the back button
        expect(getRenderedStyle(btns[1], 'display')).toBe('inline-block'); //should show the next button
        expect(getRenderedStyle(btns[2], 'display')).toBe('none'); //should NOT show the done button

        //click the next button
        dug.onNextClick();

        expect(getRenderedStyle(items[0], 'display')).toBe('none'); //should NOT show the first item
        expect(getRenderedStyle(items[1], 'display')).toBe('none'); //should NOT show the second item
        expect(getRenderedStyle(items[2], 'display')).toBe('block'); //should show the third item
        expect(getRenderedStyle(btns[0], 'display')).toBe('inline-block'); //should show the back button
        expect(getRenderedStyle(btns[1], 'display')).toBe('none'); //should NOT show the next button
        expect(getRenderedStyle(btns[2], 'display')).toBe('inline-block'); //should show the done button

        //click the back button
        dug.onBackClick();

        expect(getRenderedStyle(items[0], 'display')).toBe('none'); //should NOT show the first item
        expect(getRenderedStyle(items[1], 'display')).toBe('block'); //should show the second item
        expect(getRenderedStyle(items[2], 'display')).toBe('none'); //should NOT show the third item
        expect(getRenderedStyle(btns[0], 'display')).toBe('inline-block'); //should show the back button
        expect(getRenderedStyle(btns[1], 'display')).toBe('inline-block'); //should show the next button
        expect(getRenderedStyle(btns[2], 'display')).toBe('none'); //should NOT show the done button

        //close the window
        dug.onDoneClick();
        expect(getRenderedStyle(cont[0], 'display')).toBe('none');

        removeDom(guide); //clean up the dom
    });

    it('should handle one item', function() {
        var dug = new window.DjangoUserGuide(),
            items = null,
            btns = null,
            cont = null,
            guide = createDom([
                '<div class="django-user-guide">',
                '   <div class="django-user-guide-mask">',
                '      <div class="django-user-guide-window">',
                '           <div class="django-user-guide-close-div">x</div>',
                '           <div class="django-user-guide-html-wrapper">',
                '               <div class="django-user-guide-item"><p>Hello guide 1</p></div>',
                '           </div>',
                '           <div class="django-user-guide-window-nav">',
                '                <button class="django-user-guide-back-btn">&lt; Back</button>',
                '                <button class="django-user-guide-next-btn">Next &gt;</button>',
                '                <button class="django-user-guide-done-btn">Done</button>',
                '            </div>',
                '        </div>',
                '    </div>',
                '</div>'
            ].join('\n'));

        //add the guide to the dom
        appendDom(guide);

        //run the user guide
        dug.run();

        //examine the result
        items = queryAllDom('.django-user-guide-item');
        btns = queryAllDom('button');
        cont = queryAllDom('.django-user-guide');

        expect(getRenderedStyle(items[0], 'display')).toBe('block'); //should show the first item
        expect(getRenderedStyle(btns[2], 'display')).toBe('inline-block'); //should show the next button

        //close the window
        dug.onCloseClick();
        expect(getRenderedStyle(cont[0], 'display')).toBe('none');

        removeDom(guide); //clean up the dom
    });

    it('should handle no items', function() {
        var dug = new window.DjangoUserGuide(),
            cont = null,
            guide = createDom([
                '<div class="django-user-guide">',
                '   <div class="django-user-guide-mask">',
                '      <div class="django-user-guide-window">',
                '           <div class="django-user-guide-close-div">x</div>',
                '           <div class="django-user-guide-html-wrapper">',
                '           </div>',
                '           <div class="django-user-guide-window-nav">',
                '                <button class="django-user-guide-back-btn">&lt; Back</button>',
                '                <button class="django-user-guide-next-btn">Next &gt;</button>',
                '                <button class="django-user-guide-done-btn">Done</button>',
                '            </div>',
                '        </div>',
                '    </div>',
                '</div>'
            ].join('\n'));

        //add the guide to the dom
        appendDom(guide);

        //run the user guide
        dug.run();

        //examine the result
        cont = queryAllDom('.django-user-guide');

        expect(getRenderedStyle(cont[0], 'display')).toBe('none'); //should not show the guide

        //manaing to click the buttons should not cause trouble
        dug.onBackClick();
        dug.onNextClick();
        dug.onDoneClick();
        dug.onCloseClick();

        removeDom(guide); //clean up the dom
    });
});

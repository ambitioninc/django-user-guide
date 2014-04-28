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

    function getFakeEvt(className) {
        return {
            target: {
                className: className || ''
            },
            stopPropagation: function() {}
        };
    }

    var guideHtml = [
            '<div class="django-user-guide">',
            '   <div class="django-user-guide-mask">',
            '      <div class="django-user-guide-window">',
            '           <div class="django-user-guide-close-div">x</div>',
            '           <div class="django-user-guide-html-wrapper">',
            '           </div>',
            '           <div class="django-user-guide-counter">',
            '               <span>Tip 1 of 1</span>',
            '           </div>',
            '           <div class="django-user-guide-window-nav">',
            '                <button class="django-user-guide-btn django-user-guide-back-btn">&lt; Back</button>',
            '                <button class="django-user-guide-btn django-user-guide-next-btn">Next &gt;</button>',
            '                <button class="django-user-guide-btn django-user-guide-done-btn">Done</button>',
            '            </div>',
            '        </div>',
            '    </div>',
            '</div>'
        ].join('\n'),
        guideDom;

    beforeEach(function() {
        guideDom = createDom(guideHtml);
        appendDom(guideDom);
    });

    afterEach(function() {
        removeDom(guideDom);
    });

    it('should handle many items', function() {
        var dug = new window.DjangoUserGuide({
                csrfCookieName: 'csrf-token-custom'
            }),
            items = null,
            btns = null,
            cont = null,
            counter = null,
            guides = [
                '<div data-guide="1" class="django-user-guide-item"><p>Hello guide 1</p></div>',
                '<div data-guide="2" class="django-user-guide-item"><p>Hello guide 2</p></div>',
                '<div data-guide="3" class="django-user-guide-item"><p>Hello guide 3</p></div>',
            ].join('\n');

        //set a custom cookie
        document.cookie = 'csrf-token-custom=123456789';

        //add the guide items to the dom
        document.querySelector('.django-user-guide-html-wrapper').innerHTML = guides;

        //mock async methods
        spyOn(dug, 'put');

        //run the user guide
        dug.run();

        //examine the result
        items = queryAllDom('.django-user-guide-item');
        btns = queryAllDom('button');
        cont = queryAllDom('.django-user-guide');
        counter = queryAllDom('.django-user-guide-counter span')[0];

        expect(getRenderedStyle(items[0], 'display')).toBe('block'); //should show the first item
        expect(getRenderedStyle(items[1], 'display')).toBe('none'); //should NOT show the second item
        expect(getRenderedStyle(items[2], 'display')).toBe('none'); //should NOT show the third item
        expect(getRenderedStyle(btns[0], 'display')).toBe('none'); //should NOT show the back button
        expect(getRenderedStyle(btns[1], 'display')).toBe('inline-block'); //should show the next button
        expect(getRenderedStyle(btns[2], 'display')).toBe('none'); //should NOT show the done button
        expect(counter.innerHTML).toBe('Tip 1 of 3');

        //click the next button
        dug.onNextClick();

        expect(dug.put).toHaveBeenCalledWith(
            '/user-guide/api/guideinfo/1/', {'is_finished': true}
        ); //should make a PUT request
        expect(getRenderedStyle(items[0], 'display')).toBe('none'); //should NOT show the first item
        expect(getRenderedStyle(items[1], 'display')).toBe('block'); //should show the second item
        expect(getRenderedStyle(items[2], 'display')).toBe('none'); //should NOT show the third item
        expect(getRenderedStyle(btns[0], 'display')).toBe('inline-block'); //should show the back button
        expect(getRenderedStyle(btns[1], 'display')).toBe('inline-block'); //should show the next button
        expect(getRenderedStyle(btns[2], 'display')).toBe('none'); //should NOT show the done button
        expect(counter.innerHTML).toBe('Tip 2 of 3');

        //click the next button
        dug.onNextClick();

        expect(dug.put).toHaveBeenCalledWith(
            '/user-guide/api/guideinfo/2/', {'is_finished': true}
        ); //should make a PUT request
        expect(getRenderedStyle(items[0], 'display')).toBe('none'); //should NOT show the first item
        expect(getRenderedStyle(items[1], 'display')).toBe('none'); //should NOT show the second item
        expect(getRenderedStyle(items[2], 'display')).toBe('block'); //should show the third item
        expect(getRenderedStyle(btns[0], 'display')).toBe('inline-block'); //should show the back button
        expect(getRenderedStyle(btns[1], 'display')).toBe('none'); //should NOT show the next button
        expect(getRenderedStyle(btns[2], 'display')).toBe('inline-block'); //should show the done button
        expect(counter.innerHTML).toBe('Tip 3 of 3');

        //click the back button
        dug.onBackClick();

        expect(getRenderedStyle(items[0], 'display')).toBe('none'); //should NOT show the first item
        expect(getRenderedStyle(items[1], 'display')).toBe('block'); //should show the second item
        expect(getRenderedStyle(items[2], 'display')).toBe('none'); //should NOT show the third item
        expect(getRenderedStyle(btns[0], 'display')).toBe('inline-block'); //should show the back button
        expect(getRenderedStyle(btns[1], 'display')).toBe('inline-block'); //should show the next button
        expect(getRenderedStyle(btns[2], 'display')).toBe('none'); //should NOT show the done button
        expect(counter.innerHTML).toBe('Tip 2 of 3');

        //close the window
        dug.onCloseClick();
        expect(getRenderedStyle(cont[0], 'display')).toBe('none');
    });

    it('should handle one item', function() {
        var dug = new window.DjangoUserGuide(),
            items = null,
            btns = null,
            cont = null,
            counter = null,
            guides = [
                '<div data-guide="23" class="django-user-guide-item"><p>Hello guide 23</p></div>',
            ].join('\n');

        //add the guide items to the dom
        document.querySelector('.django-user-guide-html-wrapper').innerHTML = guides;

        //mock async methods
        spyOn(dug, 'put');

        //run the user guide
        dug.run();

        //examine the result
        items = queryAllDom('.django-user-guide-item');
        btns = queryAllDom('button');
        cont = queryAllDom('.django-user-guide');
        counter = queryAllDom('.django-user-guide-counter span')[0];

        expect(getRenderedStyle(items[0], 'display')).toBe('block'); //should show the first item
        expect(getRenderedStyle(btns[2], 'display')).toBe('inline-block'); //should show the next button
        expect(counter.innerHTML).toBe('Tip 1 of 1');

        //click done on the window
        dug.onDoneClick();
        expect(dug.put).toHaveBeenCalledWith(
            '/user-guide/api/guideinfo/23/', {'is_finished': true}
        ); //should make a PUT request
        expect(getRenderedStyle(cont[0], 'display')).toBe('none');
    });

    it('should handle no items', function() {
        var dug = new window.DjangoUserGuide(),
            cont = null;

        //mock async methods
        spyOn(dug, 'put');

        //run the user guide
        dug.run();

        //examine the result
        cont = queryAllDom('.django-user-guide');

        expect(getRenderedStyle(cont[0], 'display')).toBe('none'); //should not show the guide

        //buttons exist, but don't do anything
        expect(dug.getBackBtn()).not.toBeUndefined();
        expect(dug.getNextBtn()).not.toBeUndefined();
        expect(dug.getDoneBtn()).not.toBeUndefined();
        expect(dug.getCloseDiv()).not.toBeUndefined();
        expect(dug.getGuideMask()).not.toBeUndefined();
        expect(getRenderedStyle(dug.getBackBtn(), 'display')).toBe('none');
        expect(getRenderedStyle(dug.getDoneBtn(), 'display')).toBe('none');
        expect(getRenderedStyle(dug.getNextBtn(), 'display')).toBe('none');
        expect(getRenderedStyle(dug.getGuideMask(), 'display')).toBe('block'); //hidden by parent
        expect(getRenderedStyle(dug.getCloseDiv(), 'display')).toBe('block'); //hidden by parent

        //none of the events should cause trouble
        dug.onBackClick();
        dug.onNextClick();
        dug.onDoneClick();
        dug.onCloseClick();
        dug.onMaskClick(getFakeEvt());
        dug.onMaskClick(getFakeEvt('django-user-guide-mask'));

        expect(getRenderedStyle(cont[0], 'display')).toBe('none'); //should still be hidden
    });

    it('should get a custom csrf token', function() {
        var dug = new window.DjangoUserGuide({
            csrfCookieName: 'csrf-token-custom'
        });

        //set a custom cookie for extraction
        document.cookie = 'csrf-token-custom=123456789';
        expect(dug.getCsrfToken()).toBe('123456789');

        //look for a missing cookie
        dug.csrfCookieName = 'missing-csrf-token';
        expect(dug.getCsrfToken()).toBe('');

        //clean up the cookie
        document.cookie = 'csrf-token-custom=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    });

    it('should put data to a give url', function() {
        var dug = new window.DjangoUserGuide(),
            sendData = {
                'is_finished': true
            };

        //mock async methods and setRequestHeader
        spyOn(XMLHttpRequest.prototype, 'send');
        spyOn(XMLHttpRequest.prototype, 'setRequestHeader');

        dug.put('/', sendData);
        expect(XMLHttpRequest.prototype.setRequestHeader).toHaveBeenCalledWith('Content-Type', 'application/json');
        expect(XMLHttpRequest.prototype.send).toHaveBeenCalledWith(JSON.stringify(sendData));

        //make sure a csrf token can be set
        dug = new window.DjangoUserGuide({
            csrfCookieName: 'csrf-token-custom'
        });

        document.cookie = 'csrf-token-custom=1234';
        dug.put('/', sendData);
        expect(XMLHttpRequest.prototype.setRequestHeader).toHaveBeenCalledWith('X-CSRFToken', '1234');
        expect(XMLHttpRequest.prototype.send).toHaveBeenCalledWith(JSON.stringify(sendData));

        //clean up the cookie
        document.cookie = 'csrf-token-custom=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    });
});

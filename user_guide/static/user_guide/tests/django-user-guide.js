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
        document.cookie = 'csrf-token-custom=123456789;path=/;';

        //add the guide items to the dom
        document.querySelector('.django-user-guide-html-wrapper').innerHTML = guides;

        //mock async methods
        spyOn(dug, 'post');

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

        expect(dug.post).toHaveBeenCalledWith(
            '/user-guide/seen/', {'is_finished': true, id: 1}
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

        expect(dug.post).toHaveBeenCalledWith(
            '/user-guide/seen/', {'is_finished': true, id: 2}
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
        spyOn(dug, 'post');

        //run the user guide
        dug.run();

        //examine the result
        items = queryAllDom('.django-user-guide-item');
        btns = queryAllDom('button');
        cont = queryAllDom('.django-user-guide');
        counter = queryAllDom('.django-user-guide-counter span')[0];

        expect(getRenderedStyle(items[0], 'display')).toBe('block'); //should show the first item
        expect(getRenderedStyle(btns[2], 'display')).toBe('inline-block'); //should show the done button
        expect(counter.innerHTML).toBe('Tip 1 of 1');

        //click done on the window
        dug.onDoneClick();
        expect(dug.post).toHaveBeenCalledWith(
            '/user-guide/seen/', {'is_finished': true, id: 23}
        ); //should make a PUT request
        expect(getRenderedStyle(cont[0], 'display')).toBe('none');
    });

    it('should handle cookies instead of posts', function() {
        var dug = new window.DjangoUserGuide({
                useCookies: true
            }),
            items = null,
            btns = null,
            cont = null,
            counter = null,
            guides = [
                '<div data-guide="23" class="django-user-guide-item"><p>Hello guide 23</p></div>',
                '<div data-guide="24" class="django-user-guide-item"><p>Hello guide 24</p></div>',
            ].join('\n');

        //add the guide items to the dom
        document.querySelector('.django-user-guide-html-wrapper').innerHTML = guides;

        //mock async methods
        spyOn(dug, 'post');

        //run the user guide
        dug.run();

        //examine the result
        items = queryAllDom('.django-user-guide-item');
        btns = queryAllDom('button');
        cont = queryAllDom('.django-user-guide');
        counter = queryAllDom('.django-user-guide-counter span')[0];

        expect(getRenderedStyle(items[0], 'display')).toBe('block'); //should show the first item
        expect(getRenderedStyle(btns[1], 'display')).toBe('inline-block'); //should show the next button
        expect(getRenderedStyle(btns[2], 'display')).toBe('none'); //should not show the done button
        expect(counter.innerHTML).toBe('Tip 1 of 2');

        //click on the next button
        dug.onNextClick();
        expect(dug.post).not.toHaveBeenCalled(); //should NOT make a PUT request
        expect(dug.getCookie('django-user-guide-23')).not.toBeNull(); //should have set a cookie for guide 23

        //click done on the window
        dug.onDoneClick();
        expect(dug.post).not.toHaveBeenCalled(); //should NOT make a PUT request
        expect(dug.getCookie('django-user-guide-24')).not.toBeNull(); //should have set a cookie for guide 24
        expect(getRenderedStyle(cont[0], 'display')).toBe('none');

        //a new user guide using cookies should get no items
        dug = new window.DjangoUserGuide({
            useCookies: true
        });
        expect(dug.getItems().length).toBe(0);

        //a new user guide not using cookies should get items
        dug = new window.DjangoUserGuide({
            useCookies: false
        });
        expect(dug.getItems().length).toBe(2);

        //clear the cookies
        document.cookie = 'django-user-guide-23=;path=/;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        document.cookie = 'django-user-guide-24=;path=/;expires=Thu, 01 Jan 1970 00:00:01 GMT;';

        //a new user guide using cookies should get 2 items
        dug = new window.DjangoUserGuide({
            useCookies: true
        });
        expect(dug.getItems().length).toBe(2);

        //clean up the the cookies
        document.cookie = 'django-user-guide-23=;path=/;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        document.cookie = 'django-user-guide-24=;path=/;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    });

    it('should handle no items', function() {
        var dug = new window.DjangoUserGuide(),
            cont = null;

        //mock async methods
        spyOn(dug, 'post');

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

    it('should return empty csrf token', function() {
        var dug = new window.DjangoUserGuide();

        expect(dug.getCsrfToken()).toBe('');
    });

    it('should post data to a given url', function() {
        var dug = new window.DjangoUserGuide(),
            sendData = {
                id: 1,
                'is_finished': true
            },
            input = '<input type="hidden" name="csrfmiddlewaretoken" value="1234" />';

        //mock async methods and setRequestHeader
        spyOn(XMLHttpRequest.prototype, 'send');
        spyOn(XMLHttpRequest.prototype, 'setRequestHeader');

        dug.post('/', sendData);
        expect(XMLHttpRequest.prototype.setRequestHeader).toHaveBeenCalledWith(
            'Content-Type',
            'application/x-www-form-urlencoded; charset=UTF-8'
        );
        expect(XMLHttpRequest.prototype.send).toHaveBeenCalledWith('id=1&is_finished=true');

        //make sure a csrf token can be set
        dug = new window.DjangoUserGuide();

        //add the csrf token to the html
        document.querySelector('.django-user-guide-html-wrapper').innerHTML = input;

        dug.post('/', sendData);
        expect(XMLHttpRequest.prototype.setRequestHeader).toHaveBeenCalledWith('X-CSRFToken', '1234');
        expect(XMLHttpRequest.prototype.send).toHaveBeenCalledWith('id=1&is_finished=true');
    });
});

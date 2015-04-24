(function() {
    'use strict';

    /**
     * @constructor
     * Sets the passed csrf token name from the template.
     */
    window.DjangoUserGuide = function DjangoUserGuide(config) {
        config = config || {};
        this.useCookies = config.useCookies;
        this.finishedItems = {};
        this.itemIndex = 0;
    };

    window.DjangoUserGuide.prototype = {

        /**
         * @method getGuide
         * Gets the entire user guide div.
         * @returns {HTMLDivElement}
         */
        getGuide: function getGuide() {
            if (!this.guide) {
                this.guide = document.querySelector('.django-user-guide');
            }
            return this.guide;
        },

        /**
         * @method getGuideMask
         * Gets the guide mask.
         * @returns {HTMLDivElement}
         */
        getGuideMask: function getGuideMask() {
            if (!this.guideMask) {
                this.guideMask = document.querySelector('.django-user-guide-mask');
            }
            return this.guideMask;
        },

        /**
         * @method getItems
         * Gets the guide's html guide items.
         * @returns {HTMLDivElement[]}
         */
        getItems: function getItems() {
            if (!this.items) {
                var self = this,
                    items = Array.prototype.slice.call(
                        document.querySelectorAll('.django-user-guide-item')
                    );

                if (self.useCookies) { //only show items that do not have a cookie
                    self.items = [];

                    items.forEach(function(item) {
                        var guideId = item.getAttribute('data-guide'),
                            cookie = self.getCookie('django-user-guide-' + guideId);

                        if (!cookie) {
                            self.items.push(item);
                        }
                    });
                } else { //show all the items
                    self.items = items;
                }
            }
            return this.items;
        },

        /**
         * @method getBackBtn
         * Gets the guide's back button.
         * @returns {HTMLButtonElement}
         */
        getBackBtn: function getBackBtn() {
            if (!this.backBtn) {
                this.backBtn = document.querySelector('.django-user-guide-back-btn');
            }
            return this.backBtn;
        },

        /**
         * @method getNextBtn
         * Gets the guide's next button.
         * @returns {HTMLButtonElement}
         */
        getNextBtn: function getNextBtn() {
            if (!this.nextBtn) {
                this.nextBtn = document.querySelector('.django-user-guide-next-btn');
            }
            return this.nextBtn;
        },

        /**
         * @method getDoneBtn
         * Gets the guide's done button.
         * @returns {HTMLButtonElement}
         */
        getDoneBtn: function getNextBtn() {
            if (!this.doneBtn) {
                this.doneBtn = document.querySelector('.django-user-guide-done-btn');
            }
            return this.doneBtn;
        },

        /**
         * @method getCloseDiv
         * Gets the guide's close div.
         * @returns {HTMLDivElement}
         */
        getCloseDiv: function getCloseDiv() {
            if (!this.closeDiv) {
                this.closeDiv = document.querySelector('.django-user-guide-close-div');
            }
            return this.closeDiv;
        },

        /**
         * @method getCounterSpan
         * Gets the guide's counter span.
         * @returns {HTMLSpanElement}
         */
        getCounterSpan: function getCounterSpan() {
            if (!this.counterDiv) {
                this.counterDiv = document.querySelector('.django-user-guide-counter span');
            }
            return this.counterDiv;
        },

        /**
         * @method getCookie
         * Gets the cookie value for a given cookie name.
         * @param {String} name - The name of the cookie to get.
         */
        getCookie: function getCookie(name) {
            return document.cookie.match(new RegExp(name + '=([^;]*)'));
        },

        /**
         * @method getCsrfToken
         * Gets the csrf token as set by the cookie.
         * @returns {String}
         */
        getCsrfToken: function getCsrfToken() {
            var input = this.getGuide().querySelector('input[name=csrfmiddlewaretoken]');
            return input ? input.value : '';
        },

        /**
         * @type {Object}
         * Objects that should be shown inline-block instead of block.
         * Add more items here as needed.
         */
        inlineBlockItems: {
            'BUTTON': true
        },

        /**
         * @method hideEl
         * Hides an item.
         * @param {HTMLElement} item - The item to hide.
         */
        hideEl: function hideEl(item) {
            item.style.display = 'none';
        },

        /**
         * @method showEl
         * Shows an item. Sets the display property to 'block' unless it appears in {@link inlineBlockItems}.
         * @param {HTMLElement} item - The item to show.
         */
        showEl: function showEl(item) {
            if (this.inlineBlockItems.hasOwnProperty(item.tagName)) {
                item.style.display = 'inline-block';
            } else {
                item.style.display = 'block';
            }
        },

        /**
         * @method showHideBtns
         * Decides which buttons should be visible, then shows/hides them accordingly.
         */
        showHideBtns: function showHideBtns() {
            if (!this.getItems()[this.itemIndex + 1]) { //we have reached the end

                //there might not be a previous guide
                if (this.getItems().length > 1) {
                    this.showEl(this.getBackBtn());
                } else {
                    this.hideEl(this.getBackBtn());
                }

                this.hideEl(this.getNextBtn());
                this.showEl(this.getDoneBtn());
            } else if (!this.getItems()[this.itemIndex - 1]) { //we are at the start
                this.hideEl(this.getBackBtn());
                this.hideEl(this.getDoneBtn());
                this.showEl(this.getNextBtn());
            } else { //we are in the middle
                this.hideEl(this.getDoneBtn());
                this.showEl(this.getBackBtn());
                this.showEl(this.getNextBtn());
            }
        },

        /**
         * @method showNextGuide
         * Shows the next guide in the list of {@link items}.
         */
        showNextGuide: function showNextGuide() {
            var curr = this.getItems()[this.itemIndex],
                next = this.getItems()[this.itemIndex + 1];

            if (curr && next) {
                this.updateItemIndex(1);
                this.hideEl(curr);
                this.showEl(next);
                this.showHideBtns();
            }
        },

        /**
         * @method showPrevGuide
         * Shows the previous guide in the list of {@link items}.
         */
        showPrevGuide: function showPrevGuide() {
            var curr = this.getItems()[this.itemIndex],
                prev = this.getItems()[this.itemIndex - 1];

            if (curr && prev) {
                this.updateItemIndex(-1);
                this.hideEl(curr);
                this.showEl(prev);
                this.showHideBtns();
            }
        },

        /**
         * @method updateItemIndex
         * Updates the item index and refreshes the tool tip numbers.
         * @param {Number} num - The number to incread the {@link itemIndex} by.
         */
        updateItemIndex: function updateItemIndex(num) {
            this.itemIndex += num;

            this.getCounterSpan().innerHTML = 'Tip ' + (this.itemIndex + 1) + ' of ' + (this.getItems().length);
        },

        /**
         * @method post
         * Makes a POST request to the given url, with the given data.
         * @param {String} url - The url to POST.
         * @param {Object} data - The data to POST.
         */
        post: function post(url, data) {
            var req = new XMLHttpRequest(),
                csrfToken = this.getCsrfToken(),
                encoded = Object.keys(data).map(function(key) {
                    return encodeURIComponent(key) + '=' + encodeURIComponent(data[key]);
                }).join('&');

            //open the request
            req.open('POST', url, true);

            if (csrfToken) { //see if the csrf token should be set
                req.setRequestHeader('X-CSRFToken', csrfToken);
            }

            //send the data
            req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
            req.send(encoded);
        },

        /**
         * @method saveCookie
         * Saves a cookie for the given user guide.
         * @param {String} name - The name of the cookie to save.
         * @param {Boolean} value - The value of the cookie to save.
         */
        saveCookie: function saveCookie(name, value) {
            document.cookie = name + '=' + value + ';path=/;';
        },

        /**
         * @method isFinished
         * Describes if a particular guide has been finished. Always returns true by default.
         * Override this method for custom finish criteria logic.
         * Return true to allow the {@link finishedItem} method to proceed.
         * @param {HTMLDivElement} item - The item to check.
         * @returns {Boolean}
         */
        isFinished: function isFinished() {
            return true;
        },

        /**
         * @method finishItem
         * Marks an item finished and calls {@link post}.
         * @param {HTMLDivElement} item - The item to mark finished.
         */
        finishItem: function finishItem(item) {
            var guideId = +(item ? item.getAttribute('data-guide') : null);

            if (guideId && !this.finishedItems[guideId] && this.isFinished(item)) {
                this.finishedItems[guideId] = true;

                if (this.useCookies) { //save a cookie for the finished guide
                    this.saveCookie('django-user-guide-' + guideId, 'true');
                } else { //make a post request to mark the guide finished
                    this.post('/user-guide/seen/', {
                        'id': guideId,
                        'is_finished': true
                    });
                }
            }

            return item;
        },

        /**
         * @method show
         * Shows the entire guide.
         */
        show: function show() {
            if (this.getItems().length) { //we have some guides
                this.addListeners();
                this.updateItemIndex(0);
                this.showEl(this.getGuide());
                this.showEl(this.getItems()[0]);
                this.showHideBtns();
            }
        },

        /**
         * @method addListeners
         * Adds listeners to the various guide components.
         */
        addListeners: function addListeners() {
            this.getBackBtn().onclick = this.onBackClick.bind(this);
            this.getNextBtn().onclick = this.onNextClick.bind(this);
            this.getDoneBtn().onclick = this.onDoneClick.bind(this);
            this.getCloseDiv().onclick = this.onCloseClick.bind(this);
            this.getGuideMask().onclick = this.onMaskClick.bind(this);
        },

        /**
         * @method onCloseClick
         * Handler for clicking on the guide mask.
         */
        onMaskClick: function onMaskClick(evt) {
            if (evt.target.className === 'django-user-guide-mask') {
                this.hideEl(this.getGuide());
            }
            evt.stopPropagation();
        },

        /**
         * @method onCloseClick
         * Handler for closing the guide window.
         */
        onCloseClick: function onCloseClick() {
            this.hideEl(this.getGuide());
        },

        /**
         * @method onDoneClick
         * Handler for finishing the guide window.
         */
        onDoneClick: function onDoneClick() {
            this.finishItem(this.getItems()[this.itemIndex]);
            this.hideEl(this.getGuide());
        },

        /**
         * @method onNextClick
         * Handler for showing the next guide.
         */
        onNextClick: function onNextClick() {
            this.finishItem(this.getItems()[this.itemIndex]);
            this.showNextGuide();
        },

        /**
         * @method onBackClick
         * Handler for showing the previous guide.
         */
        onBackClick: function onBackClick() {
            this.showPrevGuide();
        },

        /**
         * @method run
         * Runs the entire process for showing the guide window.
         */
        run: function run() {
            this.show();
        }
    };
})();

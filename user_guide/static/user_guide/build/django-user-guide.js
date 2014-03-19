(function() {
    'use strict';

    window.DjangoUserGuide = function() {};

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
         * @method getItems
         * Gets the guide's html guide items.
         * @returns {HTMLDivElement[]}
         */
        getItems: function getItems() {
            if (!this.items) {
                this.items = document.querySelectorAll('.django-user-guide-item');
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
         * @type {Number}
         * The currently visible guide.
         */
        itemIndex: 0,

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
         * Shows an item. If a button
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
                this.itemIndex++;
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
                this.itemIndex--;
                this.hideEl(curr);
                this.showEl(prev);
                this.showHideBtns();
            }
        },

        /**
         * @method show
         * Shows the entire guide.
         */
        show: function show() {
            if (this.getItems().length) { //we have some guides
                this.showEl(this.getGuide());
                this.showEl(this.getItems()[0]);
                this.addListeners();
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
        onDoneClick: function onCloseClick() {
            this.hideEl(this.getGuide());
        },

        /**
         * @method onNextClick
         * Handler for showing the next guide.
         */
        onNextClick: function onNextClick() {
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
            this.addListeners();
            this.show();
        }
    };
})();

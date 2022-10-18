function ModalWindow(content, movable) {
    var context = this;

    this.locked = false;

    // these are the cursor's coordinates of
    // last drag n drop

    this.cursorX = 0;
    this.cursorY = 0;

    this.movable = (movable === undefined) ? false : movable;

    // some of working with DOM has been put into
    // closures to separate different logic

    this.overlay = (function () {
        var overlay = document.createElement('div');

        overlay.className = 'modal-overlay';

        overlay.addEventListener('click', function () {
            context.close();
        });

        return overlay;
    })();

    this.content = (function () {
        var content = document.createElement('div');

        content.className = 'modal-content';

        return content;
    })();

    this.window = (function () {
        var window = document.createElement('div');

        window.className = 'modal-window';

        var tempHandler = null;

        window.addEventListener('mousedown', function (e) {
            if (!context.movable) {
                return false;
            }

            window.classList.add('modal-moving');

            var offsetX = e.clientX - window.offsetLeft;
            var offsetY = e.clientY - window.offsetTop;

            tempHandler = function (e) {
                window.style.left = e.clientX - offsetX + 'px';
                window.style.top = e.clientY - offsetY + 'px';
            };

            document.addEventListener('mousemove', tempHandler);
        });

        window.addEventListener('mouseup', function (e) {
            if (!context.movable) {
                return false;
            }

            window.classList.remove('modal-moving');

            context.cursorX = e.clientX;
            context.cursorY = e.clientY;

            document.removeEventListener('mousemove', tempHandler);
        });

        window.appendChild(context.content);

        return window;
    })();

    // it contains all the elements of a ModalWindow
    this.layout = (function () {
        var layout = document.createElement('div');

        layout.appendChild(context.overlay);

        layout.appendChild(context.window);

        return layout;
    })();

    document.body.appendChild(this.layout);

    this.setContent(content, true);

    window.addEventListener('resize', function () {
        if (!context.movable) {
            context.centralize();
        }
    });
}

ModalWindow.prototype.show = function () {
    this.layout.style.display = 'block';

    this.centralize();

    return this;
};

ModalWindow.prototype.hide = function () {
    this.layout.style.display = 'none';

    return this;
};

ModalWindow.prototype.lock = function () {
    this.locked = true;

    return this;
};

ModalWindow.prototype.unlock = function () {
    this.locked = false;

    return this;
};

ModalWindow.prototype.allowMoving = function () {
    this.movable = true;
};

ModalWindow.prototype.denyMoving = function () {
    this.movable = false;
};

ModalWindow.prototype.close = function () {
    if (!this.locked) {
        this.layout.parentNode.removeChild(this.layout);

        this.onCloseCallback();
    }
};

ModalWindow.prototype.recalculateWidth = function () {
    // if we don't unset the width here, we would
    // get the last width, not the current one
    // when using "getBoundingClientRect().width"
    this.window.style.width = '';

    this.window.style.width = this.window.getBoundingClientRect().width + 'px';
};

ModalWindow.prototype.centralize = function () {
    var left = (document.documentElement.clientWidth - this.window.offsetWidth) / 2;

    var top = (document.documentElement.clientHeight - this.window.offsetHeight) / 2;

    this.window.style.left = left + 'px';

    this.window.style.top = top + 'px';
};

ModalWindow.prototype.setContent = function (content, centralizeMovable, keepMovablesRation) {
    if (centralizeMovable === undefined) {
        centralizeMovable = false;
    }

    if (keepMovablesRation === undefined) {
        keepMovablesRation = true;
    }

    // we don't centralize a movable window until it's been asked
    if (!this.movable || this.movable && centralizeMovable) {
        this.content.innerHTML = content;

        this.recalculateWidth();

        this.centralize();
    } else {
        if (keepMovablesRation) {
            // here, we determine what percent of the window's is
            // in the left and in the top of the cursor to keep that
            // ratio when setting new content

            var percentInLeft = (this.cursorX - this.window.offsetLeft) / this.window.clientWidth * 100;

            var percentInTop = (this.cursorY - this.window.offsetTop) / this.window.clientHeight * 100;

            this.content.innerHTML = content;

            this.recalculateWidth();

            this.window.style.left = (this.cursorX - this.window.clientWidth / 100 * percentInLeft) + 'px';

            this.window.style.top = (this.cursorY - this.window.clientHeight / 100 * percentInTop) + 'px';
        } else {
            // similarly, we keep the ration until it's been asked to not

            this.content.innerHTML = content;

            this.recalculateWidth();
        }

    }
};

ModalWindow.prototype.onCloseCallback = function () {
};

// here is the interface of setting onClose callbacks
ModalWindow.prototype.onClose = function (callback) {
    this.onCloseCallback = callback;
};
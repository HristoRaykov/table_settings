if (!window.dash_clientside) {
    window.dash_clientside = {};
}


window.dash_clientside.clientside = {
    make_draggable: function (id, children) {


        setTimeout(function () {
            // var drake = dragula({});
            // var el = document.getElementById(id);
            //
            // drake.containers.push(el);

            var el = document.getElementById(id);
            var drake = dragula([el]);


            // setTimeout(function () {
            //     var position = _el.getBoundingClientRect();
            //     const y = position.y
            //     const containerBottom = source.offsetTop + source.offsetHeight;
            //     const containerTop = source.offsetTop;
            //
            //
            //     if (containerBottom - y < 120) {
            //         source.scrollTop += 50;
            //     } else if (containerTop + y < 120) {
            //         source.scrollTop += 50;
            //     }
            // })

            drake.on("drop", function (_el, target, source, sibling) {
                // a component has been dragged & dropped
                // get the order of the ids from the DOM
                var order_ids = Array.from(target.children).map(function (child) {
                    return child.id;
                });
                // in place sorting of the children to match the new order
                children.sort(function (child1, child2) {
                    return order_ids.indexOf(child1.props.id) - order_ids.indexOf(child2.props.id)
                });

            })


            // drake.on("over", function (_el, container, source) {
            //     // setTimeout(function () {
            //     _onMouseMove(_el, container);
            //     // }, 1)
            //
            //
            // })

        }, 1)
        return window.dash_clientside.no_update
    }
}

// function _scrollDown(container, pageY) {
//     if (this.drake.dragging && pageY === this._pageY) {
//         container.scrollTop += 5;
//         setTimeout(this._scrollDown.bind(this, container, pageY), 20);
//     }
// }
//
// function _scrollUp(container, pageY) {
//     if (this.drake.dragging && pageY === this._pageY) {
//         container.scrollTop -= 5;
//         setTimeout(this._scrollUp.bind(this, container, pageY), 20);
//     }
// }

//
// document.addEventListener('mousemove', this._onMouseMove);
//
// function _onMouseMove(e) {
//     this._pageY = e.pageY;
//
//     // if (this._drake.dragging) {
//     //scroll while drag
//     const y = this._pageY;
//     const container = document.getElementById('drag_container');
//     const containerBottom = container.offsetTop + container.offsetHeight;
//     const containerTop = container.offsetTop;
//
//     if (containerBottom - y < 120) {
//         this._scrollDown(container, y);
//     } else if (containerTop + y < 120) {
//         this._scrollUp(container, y);
//     }
//     // }
// }
//
//
// // function _scrollDown(container, pageY) {
// //     if (pageY === this._pageY) {
// //         container.scrollTop += 5;
// //         setTimeout(this._scrollDown.bind(this, container, pageY), 20);
// //     }
// // }
// //
// // function _scrollUp(container, pageY) {
// //     if (pageY === this._pageY) {
// //         container.scrollTop -= 5;
// //         setTimeout(this._scrollUp.bind(this, container, pageY), 20);
// //     }
// // }
//
//
// // function _onMouseMove(e, container) {
// //
// //     //scroll while drag
// //     // const y = e.pageY;
// //     const y = e.getBoundingClientRect().y;
// //     // const container = document.getElementById('drag_container');
// //     const containerBottom = container.offsetTop + container.offsetHeight;
// //     const containerTop = container.offsetTop;
// //
// //     if (containerBottom - y < 120) {
// //         this._scrollDown(container, y);
// //     } else if (containerTop + y < 120) {
// //         this._scrollUp(container, y);
// //     }
// //
// // }
// //
// //
// // function _scrollDown(container, pageY) {
// //     container.scrollTop += 5;
// //     setTimeout(this._scrollDown.bind(this, container, pageY), 20);
// //
// // }
// //
// // function _scrollUp(container, pageY) {
// //     container.scrollTop -= 5;
// //     setTimeout(this._scrollUp.bind(this, container, pageY), 20);
// //
// // }
//
// //
// //     document.getElementById('drag_container').addEventListener('mousemove', this._onMouseMove);
// //
// // })
//
//
// // var drake = dragula([document.querySelector('#drag_container'),]);
// //
// // var scroll = autoScroll([
// //     window,
// //     document.querySelector('#drag_container'),
// // ], {
// //     margin: 20,
// //     autoScroll: function () {
// //         return this.down && drake.dragging;
// //     }
// // });
//
//
// // var script = document.createElement('script');
// // script.src = 'https://code.jquery.com/jquery-3.4.1.min.js';
// // script.type = 'text/javascript';
// // document.getElementsByTagName('head')[0].appendChild(script);
// //
//
//
// // document.getElementsByTagName('body')[0].addEventListener('wheel', function (e) {
// //     let scrollPosition: number = $('.main-panel.ps-container').scrollTop();
// //     if (e.deltaY < 0 && scrollPosition >= 100) {
// //         $('.main-panel.ps-container').scrollTop(scrollPosition - 100);
// //     }
// //     if (e.deltaY > 0) {
// //         $('.main-panel.ps-container').scrollTop(scrollPosition + 100);
// //     }
// // });

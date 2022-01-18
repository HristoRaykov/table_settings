// $(window).load(function () {
//
//     var drake = dragula({});
//     var el = document.getElementById('drag_container');
//
//     drake.containers.push(el);
//
//
//     drake.on("drop", function (_el, target, source, sibling) {
//         // a component has been dragged & dropped
//         // get the order of the ids from the DOM
//         var order_ids = Array.from(target.children).map(function (child) {
//             return child.id;
//         });
//         // in place sorting of the children to match the new order
//         children.sort(function (child1, child2) {
//             return order_ids.indexOf(child1.props.id) - order_ids.indexOf(child2.props.id)
//         });
//
//     })
//
//
//     var scroll = autoScroll([
//         window,
//         el,
//     ], {
//         margin: 20,
//         autoScroll: function () {
//             return this.down && drake.dragging;
//         }
//     });
//
// });
//

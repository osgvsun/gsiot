import * as TreeViewModule from "/scripts/tree-view.js";

window.onload = function () {

    //创建控制元素折叠展开的子菜单
    let visibilityMenu = {
        text: "Manage Visibility",
        icon: "/image/tree.png",
        submenu: []
    };
    visibilityMenu.submenu.push({
        text: "Toggle Node",
        icon: "/image/leaf.png",
        action: function (node) {
            node.toggleNode();
        },
        submenu: []
    });
    visibilityMenu.submenu.push({
        text: "Expand Node",
        icon: "/image/leaf.png",
        action: function (node) {
            node.expandNode();
        },
        submenu: []
    });
    visibilityMenu.submenu.push({
        text: "Collapse Node",
        icon: "/image/leaf.png",
        action: function (node) {
            node.collapseNode();
        },
        submenu: []
    });
    visibilityMenu.submenu.push({
        text: "Expand Subtree",
        icon: "/image/leaf.png",
        action: function (node) {
            node.expandSubtree();
        },
        submenu: []
    });
    visibilityMenu.submenu.push({
        text: "Collapse Subtree",
        icon: "/image/leaf.png",
        action: function (node) {
            node.collapseSubtree();
        },
        submenu: []
    });

    //创建控制元素删除
    let elementMenu = {
        text: "Manage Element",
        icon: "/image/tree.png",
        submenu: []
    };
    elementMenu.submenu.push({
        text: "Create Child Node",
        icon: "images/add.png",
        action: function (node) {
            node.createChildNode("Level N - Created Node", true, "images/file.png", null, null);
            node.expandNode();
        },
        submenu: []
    });
    elementMenu.submenu.push({
        text: "Delete Node",
        icon: "/image/delete.png",
        action: function (node) {
            node.removeNode();
        },
        submenu: []
    });
    elementMenu.submenu.push({
        text: "Delete Subtree",
        icon: "/image/delete.png",
        action: function (node) {
            node.removeSubTree();
        },
        submenu: []
    });

    //创建主菜单
    let menu = [visibilityMenu, elementMenu];

    //创建树
    let tree = TreeViewModule.createTree("#tree", menu);

    //创建节点
    for (let i = 1; i < 10; i++) {
        let node1 = tree.createNode(null, null, "Level 1 - Node" + i, "/image/tree.png", false, menu);
        for (let j = 1; j < 5; j++) {
            let node2 = node1.createChildNode(node1, null, "Level 2 - Node" + j, "/image/leaf.png", null, menu);
            for (let k = 1; k < 5; k++)
                node2.createChildNode(node2, null, "Level 3 - Node" + k, "/image/leaf.png", null, menu);
        }
    }

    //重绘
    tree.invalidate();
};

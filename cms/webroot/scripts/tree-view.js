let nodeCounter = 0;

export function createTree(parentDiv, menu) {

    //清空旧内容
    parentDiv = document.querySelector(parentDiv);
    parentDiv.classList.add("tree");
    parentDiv.innerHTML = "";

    //创建一个顶级节点，作为树节点
    //所有方法绑定在顶级节点上，通过tree对象可以直接调用
    let rootNode = {

        //字段
        id: "tree-node-" + (nodeCounter++),
        level: 1,
        element: null,
        childNodes: [],
        menu: menu,
        selectedNode: null,
        menuContainer: null,
        rendered: false,

        //创建一个树节点
        createNode: function (parentNode, tag, text, icon, expanded, menu) {
            //parentNode如果未指定，默认添加到根节点
            if (!parentNode)
                parentNode = rootNode;

            let node = {
                //字段
                id: "tree-node-" + (nodeCounter++),
                level: parentNode.level + 1,
                element: null,
                text: text,
                icon: icon,
                parentNode: parentNode,
                expanded: expanded,
                childNodes: [],
                menu: menu,

                //移除节点
                removeNode: function () {
                    rootNode.removeNode(this);
                },

                //展开或收起当前节点
                toggleNode: function () {
                    rootNode.toggleNode(this);
                },

                //展开节点
                expandNode: function () {
                    rootNode.expandNode(this);
                },

                //展开所有子节点
                expandSubtree: function () {
                    rootNode.expandSubtree(this);
                },

                //设置节点文本
                setText: function (text) {
                    rootNode.setText(this, text);
                },

                //折叠节点
                collapseNode: function () {
                    rootNode.collapseNode(this);
                },

                //折叠所有子节点
                collapseSubtree: function () {
                    rootNode.collapseSubtree(this);
                },

                //移除所有子节点
                removeSubTree: function () {
                    rootNode.removeSubTree(this);
                },

                //创建子节点
                createChildNode: function (parentNode, tag, text, icon, expanded, menu) {
                    return rootNode.createNode(parentNode, tag, text, icon, expanded, menu);
                }
            };

            //如果是尚未创建完成的树，等创建完毕再统一绘制
            //如果是已经创建完成的树，立刻绘制
            if (rootNode.rendered)
                rootNode.drawNode(parentNode.element, node);

            //加入父节点麾下
            parentNode.childNodes.push(node);

            return node;
        },

        //绘制树
        invalidate: function () {
            //创建对应的元素
            let rootElement = createElement("ul", null, null);
            rootNode.element = rootElement;
            parentDiv.appendChild(rootElement);
            //绘制子节点
            for (let i = 0; i < rootNode.childNodes.length; i++)
                rootNode.drawNode(rootElement, rootNode.childNodes[i]);
            if (rootNode.childNodes.length > 0)
                rootElement.lastChild.classList.add("tree-last-child");
            //标记已经绘制
            rootNode.rendered = true;
        },

        //绘制子节点
        drawNode: function (parent, node) {
            //创建节点根容器
            let nodeElement = document.createElement("li");
            nodeElement.classList.add("tree-node");
            node.element = nodeElement;
            parent.appendChild(nodeElement);

            //创建折叠图标
            let collapseElement = createImgElement(null, null, null);
            collapseElement.className = node.expanded ? "tree-toggle-on" : "tree-toggle-off";
            if (node.childNodes.length == 0)
                collapseElement.style.visibility = "hidden";
            nodeElement.appendChild(collapseElement);

            //创建图标文本容器
            let contentContainer = createElement("span", null, "tree-content");
            nodeElement.appendChild(contentContainer);

            //创建图标元素
            let iconElement = createImgElement(null, "tree-icon", node.icon);
            contentContainer.appendChild(iconElement);

            //创建文本元素
            let textElement = createElement("a", null, "tree-text");
            textElement.innerHTML = node.text;
            contentContainer.appendChild(textElement);

            //创建子节点容器
            let childContainer = createElement("ul", null, "tree-node-parent");
            nodeElement.appendChild(childContainer);

            //递归绘制子节点
            for (let i = 0; i < node.childNodes.length; i++)
                rootNode.drawNode(childContainer, node.childNodes[i]);
            if (node.childNodes.length > 0)
                childContainer.lastChild.classList.add("tree-last-child");
            if (!node.expanded)
                childContainer.style.display = "none";

            //折叠或展开节点
            collapseElement.onclick = function () {
                rootNode.toggleNode(node);
            };

            //选中节点
            contentContainer.onclick = function () {
                rootNode.selectNode(node);
            };

            //双击折叠或展开节点
            contentContainer.ondblclick = function () {
                rootNode.toggleNode(node);
            };

            //右键显示菜单
            contentContainer.oncontextmenu = function (e) {
                //阻止浏览器和其它元素响应事件
                e.preventDefault();
                e.stopPropagation();

                //选中节点，并打开菜单
                rootNode.selectNode(node);
                rootNode.createRootMenu(e, node);
                rootNode.menuContainer.style.display = "block";
            };
        },

        //设置文本
        setText: function (node, text) {
            node.text = text;
            node.element.children[1].children[1].innerHTML = text;
        },

        //展开整颗树
        expandTree: function () {
            for (let i = 0; i < this.childNodes.length; i++)
                if (this.childNodes[i].childNodes.length > 0)
                    rootNode.expandSubtree(this.childNodes[i]);
        },

        //折叠整颗树
        collapseTree: function () {
            for (let i = 0; i < this.childNodes.length; i++)
                if (rootNode.childNodes[i].childNodes.length > 0)
                    rootNode.collapseSubtree(this.childNodes[i]);
        },

        //展开子树
        expandSubtree: function (node) {
            rootNode.expandNode(node);
            for (let i = 0; i < node.childNodes.length; i++)
                rootNode.expandSubtree(node.childNodes[i]);
        },

        //折叠子树
        collapseSubtree: function (node) {
            rootNode.collapseNode(node);
            for (let i = 0; i < node.childNodes.length; i++)
                rootNode.collapseSubtree(node.childNodes[i]);
        },

        //展开节点
        expandNode: function (node) {
            if (node.childNodes.length == 0 || node.expanded)
                return;
            //更改图标
            let collapseImg = node.element.children[0];
            collapseImg.className = "tree-toggle-on";
            //显示子节点
            let childContainer = node.element.children[2];
            childContainer.style.display = "block";
            //更改状态
            node.expanded = true;
        },

        //折叠节点
        collapseNode: function (node) {
            if (node.childNodes.length == 0 || !node.expanded)
                return;
            //更改图标
            let collapseImg = node.element.children[0];
            collapseImg.className = "tree-toggle-off";
            //显示子节点
            let childContainer = node.element.children[2];
            childContainer.style.display = "none";
            //更改状态
            node.expanded = false;
        },

        //展开或折叠节点
        toggleNode: function (node) {
            if (node.childNodes.length == 0)
                return;
            if (node.expanded)
                node.collapseNode();
            else
                node.expandNode();
        },

        //选中节点
        selectNode: function (node) {
            //去除上个选中节点样式
            if (rootNode.selectedNode != null)
                rootNode.selectedNode.element.children[1].classList.remove("tree-content-selected");
            //为当前节点添加选中样式
            let contentContainer = node.element.children[1];
            contentContainer.classList.add("tree-content-selected");
            //更新选中节点
            rootNode.selectedNode = node;
        },

        //删除节点
        removeNode: function (node) {
            let index = node.parentNode.childNodes.indexOf(node);
            //移除节点
            node.element.parentNode.removeChild(node.element);
            node.parentNode.childNodes.splice(index, 1);
            //更新折叠图标
            if (node.parentNode.childNodes.length == 0) {
                let collapseImg = node.parentNode.element.children[0];
                collapseImg.style.visibility = "hidden";
            }
            //更新最后节点的样式
            if (node.parentNode.childNodes.length > 0)
                node.parentNode.childNodes[index - 1].element.classList.add("tree-last-child");
        },

        //删除整个子树
        removeSubTree: function (node) {
            if (node.childNodes.length == 0)
                return;
            //隐藏折叠图标
            let collapseImg = node.element.children[0];
            collapseImg.style.visibility = "hidden";
            //清除子节点
            node.childNodes = [];
            let childContainer = node.element.children[2];
            childContainer.innerHTML = "";
        },

        //设置右键菜单
        createRootMenu: function (event, node) {
            //TODO
            if (!node.menu)
                return;

            //创建菜单容器
            if (rootNode.menuContainer == null) {
                rootNode.menuContainer = createElement("ul", null, null);
                rootNode.menuContainer.classList.add("tree-menu-container");
                rootNode.menuContainer.classList.add("tree-menu-parent");
                document.body.appendChild(rootNode.menuContainer);
            }

            //清除旧的菜单内容
            rootNode.menuContainer.innerHTML = "";

            //设置菜单位置
            let left = event.pageX - 5;
            let right = event.pageY - 5;
            rootNode.menuContainer.style.left = left + "px";
            rootNode.menuContainer.style.top = right + "px";

            //逐个创建菜单节点
            for (let i = 0; i < node.menu.length; i++)
                rootNode.createMenu(rootNode.menuContainer, node.menu[i], node);
        },

        //创建菜单
        createMenu: function (parentElement, menu, node) {
            //创建菜单容器
            let menuContainer = createElement("li", null, null);
            menuContainer.classList.add("tree-menu");
            parentElement.appendChild(menuContainer);
            if (!menu.submenu.length)
                menuContainer.onclick = function () {
                    menu.action(node);
                };

            //创建菜单图标
            let iconImg = createImgElement(null, null, menu.icon);
            menuContainer.appendChild(iconImg);
            if (!menu.icon)
                iconImg.src = "image/menu.png";

            //创建文本标题
            let textElement = createElement("a", null, null);
            textElement.appendChild(document.createTextNode(menu.text));
            menuContainer.appendChild(textElement);

            //创建下级菜单图标
            let subMenuIcon = createImgElement(null, "tree-menu-icon", "image/next.png");
            menuContainer.appendChild(subMenuIcon);
            if (!menu.submenu || !menu.submenu.length)
                subMenuIcon.src = "image/hand.png";

            //创建子菜单容器
            let subMenuContainer = createElement("ul", null, null);
            subMenuContainer.classList.add("tree-menu-parent");
            menuContainer.appendChild(subMenuContainer);

            //递归创建子菜单
            if (menu.submenu)
                for (let i = 0; i < menu.submenu.length; i++)
                    rootNode.createMenu(subMenuContainer, menu.submenu[i], node);

            //无子菜单，则执行菜单事件
            if (!menu.submenu)
                node.element.onclick = () => menu.action(node);
        }
    };

    //隐藏菜单
    window.addEventListener("click", () => {
        if (rootNode.menuContainer != null)
            rootNode.menuContainer.style.display = "none";
    }, false);

    return rootNode;
}

//创建一个标签
function createElement(type, id, clazz) {
    let element = document.createElement(type);
    if (id) element.id = id;
    if (clazz) element.className = clazz;
    return element;
}

//创建一个img标签
function createImgElement(id, clazz, src) {
    let element = document.createElement("img");
    if (id) element.id = id;
    if (clazz) element.className = clazz;
    if (src) element.src = src;
    return element;
}

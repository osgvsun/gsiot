
var keyboard = function (e) {
    this.Input = null;
    this.activeInputElement = null;
    this.CapsLock_flag = false;
    this.shift_flag = false;
    objBack = new Element()
    if (e == null) e = document.body;
    objBack.Parent(e)
    objBack.Width(630)
    objBack.Height(210)
    objBack.Style.board = 1
    objBack.BackColor("#eee")
    key = {}
    key.list = [
        { "key": "key_r2c1", "text": "~<br>`" },
        { "key": 'key_1', "text": "!<br>1" },
        { "key": 'key_2', "text": "@<br>2" },
        { "key": 'key_3', "text": "#<br>3" },
        { "key": 'key_4', "text": "$<br>4" },
        { "key": 'key_5', "text": "%<br>5" },
        { "key": 'key_6', "text": "^<br>6" },
        { "key": 'key_7', "text": "&<br>7" },
        { "key": 'key_8', "text": "*<br>8" },
        { "key": 'key_9', "text": "(<br>9" },
        { "key": 'key_0', "text": ")<br>0" },
        { "key": 'key_r2c2', "text": "_<br>-" },
        { "key": 'key_r2c3', "text": "+<br>=" },
        { "key": "key_backspace", "text": "Backspace", "width": 74 },
        { "key": 'key_tab', "text": "Tab", "width": 56 },
        { "key": 'key_q', "text": "Q<br>q" },
        { "key": 'key_w', "text": "W<br>w" },
        { "key": 'key_e', "text": "E<br>e" },
        { "key": 'key_r', "text": "R<br>r" },
        { "key": 'key_t', "text": "T<br>t" },
        { "key": 'key_y', "text": "Y<br>y" },
        { "key": 'key_u', "text": "U<br>u" },
        { "key": 'key_i', "text": "I<br>i" },
        { "key": 'key_o', "text": "O<br>o" },
        { "key": 'key_p', "text": "P<br>p" },
        { "key": 'key_r3c1', "text": "{<br>[" },
        { "key": 'key_r3c2', "text": "}<br>]" },
        { "key": "key_r3c3", "text": "|<br>\\", "width": 50 },
        { "key": 'key_capslock', "text": "CapsLock", "width": 68 },
        { "key": 'key_a', "text": "A<br>a" },
        { "key": 'key_s', "text": "S<br>s" },
        { "key": 'key_d', "text": "D<br>d" },
        { "key": 'key_f', "text": "F<br>f" },
        { "key": 'key_g', "text": "G<br>g" },
        { "key": 'key_h', "text": "H<br>h" },
        { "key": 'key_j', "text": "J<br>j" },
        { "key": 'key_k', "text": "K<br>k" },
        { "key": 'key_l', "text": "L<br>l" },
        { "key": 'key_r4c1', "text": ":<br>;" },
        { "key": 'key_r4c2', "text": "\"<br>'" },
        { "key": "key_enter", "text": "Enter<br>↵", "width": 80 },
        { "key": 'key_leftshift', "text": "Shift", "width": 90 },
        { "key": 'key_z', "text": "Z<br>z" },
        { "key": 'key_x', "text": "X<br>x" },
        { "key": 'key_c', "text": "C<br>c" },
        { "key": 'key_v', "text": "V<br>v" },
        { "key": 'key_b', "text": "B<br>b" },
        { "key": 'key_n', "text": "N<br>n" },
        { "key": 'key_m', "text": "M<br>m" },
        { "key": 'key_r5c1', "text": "<<br>," },
        { "key": 'key_r5c2', "text": "><br>." },
        { "key": 'key_r5c3', "text": "?<br>/" },
        { "key": 'key_rightshift', "text": "Shift", "width": 100 },
        // {"key":"key_leftctrl","width":56,"text":"Ctrl"},
        // {"key":"key_leftwin","width":44,"text":"Win"},
        // {"key":"key_leftalt","width":44,"text":"Alt"},
        { "key": "key_space", "width": 620, "text": "<center>Space</center>" }
        // {"key":"key_rightalt","width":44,"text":"Alt"},
        // {"key":"key_rightwin","width":44,"text":"Win"},
        // {"key":"key_shortcut","width":44,"text":"Cut"},
        // {"key":"key_rightctrl","width":56,"text":"Ctrl"}
    ];
    this.showLine = function (record) {
        for (i = 0; i < record.length; i++) {
            key[record[i].key] = new Element(); o = key[record[i].key]; o.hWnd.setAttribute("id", record[i].key); o.className("key_normal"); o.Parent(objBack); o.Html(record[i].text)
            if ("width" in record[i]) o.Width(record[i].width); self = this
            o.Click(function () {
                if (this.id == "key_capslock") {
                    if (this.className == "key_checked") {
                        this.className = "key_normal"; self.CapsLock_flag = false;
                    } else {
                        this.className = "key_checked"; self.CapsLock_flag = true;
                    } $("#key_leftshift").className("key_normal"); $("#key_rightshift").className("key_normal");
                } else if (this.id == "key_rightshift" || this.id == "key_leftshift") {
                    this.className = "key_checked";
                    self.shift_flag = true;
                } else if (this.id == "key_space") {
                    self.InsertString(window.activeInputElement, " ");
                } else if (this.id == "key_enter") {
                    self.InsertString(window.activeInputElement, "\r\n");
                } else if (this.id == "key_backspace") {
                    self.DeleteString(window.activeInputElement);
                } else if (this.id == "key_tab") {
                    self.InsertString(window.activeInputElement, "\t");
                } else {
                    str = this.innerHTML.split("<br>");
                    if (self.shift_flag == true || self.CapsLock_flag == true) {
                        value = str[0]; $("#key_leftshift").className("key_normal"); $("#key_rightshift").className("key_normal"); self.shift_flag = false;
                    }
                    else if (self.shift_flag == false) value = str[1]
                    self.InsertString(window.activeInputElement, value);
                }
            })
        }
    }
    this.DeleteString = function (tb) {
        tb.focus();
        var newstart = tb.selectionStart - 1;
        tb.value = tb.value.substr(0, tb.selectionStart - 1) + tb.value.substring(tb.selectionEnd);
        tb.selectionStart = newstart;
        tb.selectionEnd = newstart;
    }
    this.InsertString = function (tb, str) {
        tb.focus();
        if (document.all) {
            var r = document.selection.createRange();
            document.selection.empty();
            r.text = str;
            r.collapse();
            r.select();
        }
        else {
            var newstart = tb.selectionStart + str.length;
            tb.value = tb.value.substr(0, tb.selectionStart) + str + tb.value.substring(tb.selectionEnd);
            tb.selectionStart = newstart;
            tb.selectionEnd = newstart;
        }
    }
    this.GetSelection = function (tbid) {

        var sel = '';
        if (document.all) {
            var r = document.selection.createRange();
            document.selection.empty();
            sel = r.text;
        }
        else {
            var tb = document.getElementById(tbid);
            // tb.focus();
            var start = tb.selectionStart;
            var end = tb.selectionEnd;
            sel = tb.value.substring(start, end);
        }
        return sel;
    }
    this.ShowSelection = function (tbid) {
        var sel = GetSelection(tbid);
        if (sel) return sel;
        else return null;
    }
    this.showLine(key.list);
    console.log(key)
    //key_r2c1=new Element();key_r2c1.className("key_normal");key_r2c1.Parent(objBack);key_r2c1.Html("~<br>`")
}


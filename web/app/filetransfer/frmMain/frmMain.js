App.Forms.frmMain.code=function(name,p){
    Form.call(this,name);this.parent=p;self=this;this.SystemPath="/api/getsystemfolder".LoadJson()
    this.Left={Name:"Left",data:{},Address:this.SystemPath.rootpath.replace("/src","")+this.SystemPath.webroot,pan:null,panTool:null,panWork:null,txtAddress:null,cmdGO:null,cmdRefresh:null};
    this.Right={Name:"Right",data:{},Address:"/media/pi",pan:null,panTool:null,panWork:null,txtAddress:null,cmdGO:null,cmdRefresh:null}
    this.load=function(){this.tmpl=App.path+"/frmMain/frmMain.txt";Document.LoadCSS(App.path+"/frmMain/global.css");Document.LoadCSS(App.rootpath+"css/gvsun.webui.css");}
    this.Form_Show=function(){
        App.frm=this;this.pan={};this.pan.conttype=(App.path+"/images/index.json").LoadJson();
        this.pan.Exit=new Element.Item(this.parent.Children(0));
        this.pan.Exit.Text("X");this.pan.Exit.align("right");
        this.pan.Exit.Click(function(){window.close()});
        with(this.Left){
            pan=this.parent.Children(1);panTool=pan.Children(0);panWork=pan.Children(1);txtAddress=$$("#leftAddress").val(Address);cmdGO=$$("#leftGo");cmdRefresh=$$("#leftRefresh");
            cmdGO.Click(function(){self.ListView(self.Left);});
            cmdRefresh.Click(function(){self.ListView(self.Left);});
        }
        with(this.Right){
            pan=this.parent.Children(2);panTool=pan.Children(0);panWork=pan.Children(1);txtAddress=$$("#rightAddress").val(this.Right.Address);cmdGO=$$("#rightGo");cmdRefresh=$$("#rightRefresh");
            cmdGO.Click(function(){self.ListView(self.Right);});
            cmdRefresh.Click(function(){self.ListView(self.Right);});
        }
        this.Left.cmdGO.Click();this.Right.cmdGO.Click();
        this.Form_Resize(Document.Width(),Document.Height());
    }
    this.changeAddress=function(key,address){
        this[key].txtAddress.val(address);
        this.ListView(this[key])
    }
    this.delItem=function(key,address){
        url=App.rootpath+"api/delfile/"+address.base64encode();
        console.log(url);result=url.LoadJson();console.log(result);
        //刷新
        if(result.result)this.ListView(this[key]);msgbox("删除完成",3);
    }
    this.copyItem=function(key,address,id){
        d="Left";if(key=="Left")d="Right";
        console.log(address);console.log(this[d].txtAddress.val());
        if(this[key].txtAddress.val()==this[d].txtAddress.val()){msgbox("源和目标地址相同，不能复制",3)}
        else{
            if(id!=null && (id in this[d].data.result)){msgbox("源和目标地址相同，不能复制",3);return null;}
            //复制
            console.log(App.rootpath+"api/cp/"+address+"/"+this[d].txtAddress.val());
            url=App.rootpath+"api/cp/"+address.base64encode()+"/"+this[d].txtAddress.val().base64encode()
            console.log(url);result=url.LoadJson();console.log(result);
            //刷新
            if(result.result)this.ListView(this[d]);msgbox("复制完成",3);
        }
    }
    this.ListView=function(obj){
        url=obj.txtAddress.val().base64encode();
        obj.data=("/api/folder/"+url).LoadJson();obj.data.result.Name=obj.Name;
        obj.data.result.isroot=!(obj.txtAddress.val()>obj.Address);/*console.log(obj.data);*/
        with(obj.panWork){
            Tmpl((App.path+"/frmMain/list.txt").LoadURL(),obj.data)
            // Children(0).Children(0).Children(0).Children(1).css("width","108px")
            // Children(0).Children(0).Children(0).Children(2).css("width","60px")
        }
        // obj.Tmpl((App.path+"/frmMain/list.txt").LoadURL(),("/api/folder/"+url).LoadJson())
        // App.frm.Left.panWork.Children(0).Children(0).Children(0).Children(0).css("width","220px")
    }
    this.Form_Resize=function(w,h){
        var toolheight=80;
        this.Left.pan.css({"width":(w/2+2)+"px","height":(h)+"px"})
        this.Left.panTool.css("height",toolheight+"px")
        this.Left.panWork.css({"height":(h-toolheight-30)+"px","overflow":"auto"})
        this.Right.pan.css({"width":(w/2+2)+"px","height":h+"px"})
        this.Right.panTool.css("height",toolheight+"px")
        this.Right.panWork.css({"height":(h-toolheight-30)+"px","overflow":"auto"})
    }
}
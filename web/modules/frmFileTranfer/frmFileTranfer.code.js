var self = this;Form.call(this, name);this.app = app; this.parent = app.parent; 
this.SystemPath="/api/getsystemfolder".LoadJson();
this.Left={Name:"Left",data:{},Address:this.SystemPath.rootpath.replace("/src","")+this.SystemPath.webroot,pan:null,panTool:null,panWork:null,txtAddress:null,cmdGO:null,cmdRefresh:null};
this.Right={Name:"Right",data:{},Address:"/media/pi",pan:null,panTool:null,panWork:null,txtAddress:null,cmdGO:null,cmdRefresh:null};
this.load=function(){
    self = this.app.Forms[this.Name];
    self.tmpl=self.app.path+"/frmFileTranfer/frmFileTranfer.txt";
    Document.LoadCSS(self.app.rootpath+"/css/gvsun.webui.css");
};
this.Form_Show=function(){
    self.app.Forms.activeForm=this;this.pan={};
    this.pan.conttype=(self.app.path+"/frmFileTranfer/images/index.json").LoadJson();
    this.pan.Exit=new Element.Item(this.parent.Children(0));
    this.pan.Exit.Text("X");this.pan.Exit.align("right");
    this.pan.Exit.Click(function(){window.close()});
    with(self.app.Forms.activeForm.Left){
        pan=this.parent.Children(1);panTool=pan.Children(0);panWork=pan.Children(1);txtAddress=$$("#leftAddress").val(Address);cmdGO=$$("#leftGo");cmdRefresh=$$("#leftRefresh");
        cmdGO.Click(function(){self.app.Forms.activeForm.ListView(self.app.Forms.activeForm.Left);});
        cmdRefresh.Click(function(){self.app.Forms.activeForm.ListView(self.app.Forms.activeForm.Left);});
    }
    with(self.app.Forms.activeForm.Right){
        pan=this.parent.Children(2);panTool=pan.Children(0);panWork=pan.Children(1);txtAddress=$$("#rightAddress").val(this.Right.Address);cmdGO=$$("#rightGo");cmdRefresh=$$("#rightRefresh");
        cmdGO.Click(function(){self.app.Forms.activeForm.ListView(self.app.Forms.activeForm.Right);});
        cmdRefresh.Click(function(){self.app.Forms.activeForm.ListView(self.app.Forms.activeForm.Right);});
    }
    this.Left.cmdGO.Click();this.Right.cmdGO.Click();
    this.Form_Resize(Document.Width(),Document.Height());
    return this;
};
this.setTitle=function(flag){
    $$("#panwork").FindElement("div").Index(0).Hide();
    if(flag)$$("#panwork").FindElement("div").Index(0).Show();
    this.Form_Resize(Document.Width(),Document.Height());
    return this;
};
this.changeAddress=function(key,address){
    this[key].txtAddress.val(address);
    this.ListView(this[key])
};
this.delItem=function(key,address){
    url=self.app.rootpath+"/api/delfile/"+address.base64encode();
    console.log(url);result=url.LoadJson();console.log(result);
    //刷新
    if(result.result)this.ListView(this[key]);msgbox("删除完成",3);
};
this.copyItem=function(key,address,id){
    d="Left";if(key=="Left")d="Right";
    if(this[key].txtAddress.val()==this[d].txtAddress.val()){msgbox("源和目标地址相同，不能复制",3)}
    else{
        if(id!=null && (id in this[d].data.result)){msgbox("源和目标地址相同，不能复制",3);return null;}
        //复制
        url=self.app.rootpath+"/api/cp/"+address.base64encode()+"/"+this[d].txtAddress.val().base64encode()
        console.log(url);result=url.LoadJson();console.log(result);
        //刷新
        if(result.result)this.ListView(this[d]);msgbox("复制完成",3);
    }
};
this.ListView=function(obj){
    url=obj.txtAddress.val().base64encode();
    obj.data=(self.app.rootpath+"/api/folder/"+url).LoadJson();obj.data.result.Name=obj.Name;
    obj.data.result.isroot=!(obj.txtAddress.val()>obj.Address);
    with(obj.panWork){
        Tmpl((self.app.path+"/frmFileTranfer/list.txt").LoadURL(),obj.data)
    }
    
};
this.Form_Resize=function(w,h){
    var toolheight=80,titleheight=0;
    if($$("#panwork").FindElement("div").Index(0).css("display")=="block"){
        titleheight=$$("#panwork").FindElement("div").Index(0).Height();
    }
    this.Left.pan.css({"width":(w/2)+"px","height":(h-90)+"px"});
    this.Left.panTool.css("height",toolheight+"px");
    this.Left.panWork.css({"height":(h-toolheight-titleheight-90)+"px","overflow":"auto"});
    this.Right.pan.css({"width":(w/2)+"px","height":(h-90)+"px"});
    this.Right.panTool.css("height",toolheight+"px");
    this.Right.panWork.css({"height":(h-toolheight-titleheight-90)+"px","overflow":"auto"});
};
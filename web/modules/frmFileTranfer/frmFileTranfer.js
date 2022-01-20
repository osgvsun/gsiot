App.code.debug.frmFileTranfer.code = function (name, app) {
    var self = this;Form.call(this, name);this.app = app; this.parent = app.parent; 
    this.SystemPath="/api/getsystemfolder".LoadJson();

    this.RightFold = true;
    this.statu=false;
    
    this.SystemPath.rootpath=this.SystemPath.rootpath.replace("/src","")
    this.SystemPath.webroot=this.SystemPath.rootpath+this.SystemPath.webroot
    this.SystemPath.webdata=this.SystemPath.webroot+"/data/inspection"
    this.SystemPath.logdata=this.SystemPath.rootpath+"/etc/log"
    this.SystemPath.configdata=this.SystemPath.rootpath+"/etc/conf"
    this.SystemPath.dbuser=this.SystemPath.rootpath+"/etc/conf/db"
    this.roots=[];
    this.Left={Name:"Left",data:{},Address:"",pan:null,panTool:null,panWork:null,txtAddress:null,cmdGO:null,cmdRefresh:null};
    this.Right={Name:"Right",data:{},Address:"/media/pi",pan:null,panTool:null,panWork:null,txtAddress:null,cmdGO:null,cmdRefresh:null};
    this.load=function(){
        self = this.app.Forms[this.Name];
        self.tmpl=self.app.path+"/frmFileTranfer/frmFileTranfer.txt";
        Document.LoadCSS(self.app.rootpath+"/css/gvsun.webui.css");
    };
    //当处于文件传输界面时进行刷新管理
    if(this.Name == "frmFileTranfer"){
         //每5秒刷新右侧文件管理
         setInterval(f,5000);   
    }   
    function f(){
        if(self.statu){
             self.app.Forms.activeForm.ListView(self.app.Forms.activeForm.Right);
            }      
    }
  
    this.Form_Show=function(){
        this.app.Forms.activeForm=this;this.pan={};
        this.app.wsc.SendMessage({"cmd":"stop detect face"})
        self.statu=true;
        self.roots=[];
       
        self.app.policy.data.ForEach(function(item){
            devIndex=item.devindex
            if(devIndex==self.app.cfg.release.device.id){
                self.roots=[];
                self.roots.Add({"expfile":self.SystemPath.webdata});
                self.roots.Add({"log":self.SystemPath.logdata});
                self.roots.Add({"conf":self.SystemPath.configdata});
                return true;
            }else{
                path=self.SystemPath.webdata+item.devindex.replace(self.app.cfg.release.device.id,"").replace(/_/g,"/")
                console.log(devIndex);console.log(path);data={};data[devIndex]=path;self.roots.Add(data)}
        });
       
        this.setRootCommand("　公共开放实验项目　",self.SystemPath.webdata);
        this.roots.ForEach(function(item){for(var key in item){this.setRootCommand(key,item[key])}});        
        this.setRootCommand("　系统日志　",this.SystemPath.logdata);
        this.pan.conttype=(self.app.path+"/frmFileTranfer/images/index.json").LoadJson();
        this.pan.Exit=new Element.Item(this.parent.Children(0));
        this.pan.Exit.Text("X");this.pan.Exit.align("right");
        this.pan.Exit.Click(function(){window.close()});
        with(self.app.Forms.activeForm.Left){
            pan=this.parent.Children(1);panTool=pan.Children(0);panWork=pan.Children(1);txtAddress=$$("#leftAddress").val(Address);

            //根据输入地址进行跳转的实现   而可删除
            cmdGO=$$("#leftGo");cmdRefresh=$$("#leftRefresh");
            cmdGO.Click(function(){self.app.Forms.activeForm.ListView(self.app.Forms.activeForm.Left);});
            cmdRefresh.Click(function(){self.app.Forms.activeForm.ListView(self.app.Forms.activeForm.Left);});
            //


        }
        with(self.app.Forms.activeForm.Right){
            pan=this.parent.Children(2);panTool=pan.Children(0);panWork=pan.Children(1);txtAddress=$$("#rightAddress").val(this.Right.Address);
        

            //根据输入地址进行跳转的实现   而可删除
            cmdGO=$$("#rightGo");cmdRefresh=$$("#rightRefresh");
            cmdGO.Click(function(){self.app.Forms.activeForm.ListView(self.app.Forms.activeForm.Right);});
            cmdRefresh.Click(function(){self.app.Forms.activeForm.ListView(self.app.Forms.activeForm.Right);});
            //
        }
        $$("#leftRoots").FindElement("button").Index(0).hWnd.click();       
        this.Form_Resize(Document.Width(),Document.Height());
        return this;
    };
    //设置主要功能按钮
    this.setRootCommand=function(text,path){
        //为每个按钮设置根目录
       // this.Left.Address=path
        console.log(this.Left.Address);
        o=$$("#leftRoots").CreatesubElement("button").css("height","40px");
        o.hWnd.innerText=text;
        //设置被选中标签的属性和值
        o.attr("onclick","App.Forms.activeForm.changeAddress('Left','"+path+"');App.Forms.activeForm.setRoot(                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      '"+path+"')")
    }
    this.setRoot = function(path){
        this.Left.Address=path;
    }
    this.setTitle=function(flag){
        $$("#panwork").FindElement("div").Index(0).Hide();
        if(flag)$$("#panwork").FindElement("div").Index(0).Show();
        this.Form_Resize(Document.Width(),Document.Height());
        return this;
    };
    this.changeAddress=function(key,address){
        this[key].txtAddress.val(address);
        this.ListView(this[key])
        console.log(this[key]);
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
    //文件目录循环遍历显示
    this.ListView=function(obj){
        console.log(obj);
        url=obj.txtAddress.val().base64encode();
        obj.data=(self.app.rootpath+"/api/folder/"+url).LoadJson();obj.data.result.Name=obj.Name;
        obj.data.result.isroot=!(obj.txtAddress.val()>obj.Address);
        with(obj.panWork){
            Tmpl((self.app.path+"/frmFileTranfer/list.txt").LoadURL(),obj.data)
            
        }
        //self.RightFold判断在/media/pi目录下是否有U盘插入
        if(obj.Name == "Right" && JSON.stringify(obj.data.result.folder) == '{}'){
            self.RightFold = false;
            console.log(self.RightFold)
        }else{
            self.RightFold = true;
        }
        //obj.txtAddress.val() 是判断当前显示路径是否是根目录
        if(!self.RightFold && obj.Name == "Right"&&obj.txtAddress.val() == "/media/pi"){
            msgbox("请插入U盘使用",3)
            window.setTimeout(function(){
                path = window.location.href;
                window.location.href = path + "/../index.html"
            },2500);	
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
}
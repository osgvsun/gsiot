App.Forms.frmSystem.code=function(name,app){
    Form.call(this,name);this.parent=app.parent;self=this;
    this.load=function(){
		this.parent.CSS("color","#ffffff")
        this.cfgFile=new JsonFile(App.rootpath+"/api/file/"+(App.cfg.rootpath+"/etc/conf/release.json").base64encode())
        this.binddata=this.cfgFile.data

	}
    this.Form_Show=function(){
        this.app.Forms.activeForm = this;
		this.app.wsc.SendMessage({"cmd":"stop detect face"})
		this.parent.Clear().Text(JSON.stringify(this.cfgFile.data,null,2))
        this.Form_Resize(Document.Width(),Document.Height());
    }
    this.Form_Resize=function(w,h){}
    this.Form_Receive = function (data) {
        console.log(this.Name + " receive:" + JSON.stringify(data))

    }
}
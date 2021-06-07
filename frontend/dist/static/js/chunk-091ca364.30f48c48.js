(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-091ca364"],{1111:function(e,t,r){"use strict";r.r(t);var a=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("el-dialog",{attrs:{title:"Add new FTSI",visible:e.dialogVisible,width:"800px","close-on-click-modal":!1},on:{"update:visible":function(t){e.dialogVisible=t},close:e.addDialogClose}},[r("span",[r("el-form",{ref:"addFormRef",attrs:{"label-width":"150px",model:e.addForm,rules:e.addFormRules}},[r("el-form-item",{staticClass:"required",attrs:{label:"FTSI Number",prop:"ftsi_num"}},[r("el-input",{staticClass:"shortInputForm",attrs:{disabled:e.pendingFlag},model:{value:e.addForm.ftsi_num,callback:function(t){e.$set(e.addForm,"ftsi_num",t)},expression:"addForm.ftsi_num"}})],1),r("el-form-item",{staticClass:"required",attrs:{label:"Rev.",prop:"rev"}},[r("el-input",{staticClass:"shortInputForm",attrs:{disabled:e.pendingFlag},model:{value:e.addForm.rev,callback:function(t){e.$set(e.addForm,"rev",t)},expression:"addForm.rev"}})],1),r("el-form-item",{staticClass:"required",attrs:{label:"Issue Date",prop:"issueDate",rules:[{required:!0,message:"please choose the start date",trigger:"blur"}]}},[r("el-date-picker",{staticStyle:{width:"190px"},attrs:{type:"date",disabled:e.pendingFlag,placeholder:"Choose date",format:"yyyy-MM-dd","value-format":"yyyy-MM-dd"},model:{value:e.addForm.issueDate,callback:function(t){e.$set(e.addForm,"issueDate",t)},expression:"addForm.issueDate"}})],1),r("el-form-item",{attrs:{label:"FTSI Title",prop:"ftsi_title"}},[r("el-input",{staticClass:"longInputForm",attrs:{type:"textarea",disabled:e.pendingFlag},model:{value:e.addForm.ftsi_title,callback:function(t){e.$set(e.addForm,"ftsi_title",t)},expression:"addForm.ftsi_title"}})],1),r("el-form-item",{attrs:{label:"Compliance Stat.",prop:"statement"}},[r("el-input",{staticClass:"longInputForm",attrs:{type:"textarea",disabled:e.pendingFlag},model:{value:e.addForm.statement,callback:function(t){e.$set(e.addForm,"statement",t)},expression:"addForm.statement"}})],1),r("el-form-item",{staticClass:"required",attrs:{label:"Monitor Type",prop:"dep_type"}},[r("el-select",{attrs:{placeholder:"Please choice"},on:{change:e.monitorTypeCheck},model:{value:e.addForm.dep_type,callback:function(t){e.$set(e.addForm,"dep_type",t)},expression:"addForm.dep_type"}},e._l(e.monitorType,(function(e){return r("el-option",{attrs:{label:e[1],value:e[0]}})})),1)],1),r("div",{directives:[{name:"show",rawName:"v-show",value:e.showCustomizeForm,expression:"showCustomizeForm"}],staticClass:"customizeForm"},[r("el-form-item",{attrs:{label:"Trigger"}},[r("el-col",{attrs:{span:9}},[r("el-form-item",{attrs:{prop:"customizePara.trigger.type"}},[r("el-select",{attrs:{placeholder:"Please choice"},on:{change:e.paraShowControl},model:{value:e.addForm.customizePara.trigger.type,callback:function(t){e.$set(e.addForm.customizePara.trigger,"type",t)},expression:"addForm.customizePara.trigger.type"}},e._l(e.triggerType,(function(e){return r("el-option",{attrs:{label:e[1],value:e[0]}})})),1)],1)],1),r("el-col",{attrs:{span:13}},[r("div",{directives:[{name:"show",rawName:"v-show",value:e.showTriggerFTSI,expression:"showTriggerFTSI"}]},[r("el-form-item",{staticClass:"required",attrs:{label:"FTSI num.",prop:"customizePara.trigger.parameter",rules:[{required:e.showTriggerFTSI,message:"please enter the related FTSI",trigger:"blur"},{validator:e.onlyNum}]}},[r("el-input",{staticClass:"shortInputForm",model:{value:e.addForm.customizePara.trigger.parameter,callback:function(t){e.$set(e.addForm.customizePara.trigger,"parameter",t)},expression:"addForm.customizePara.trigger.parameter"}})],1)],1),r("div",{directives:[{name:"show",rawName:"v-show",value:e.showTriggerDate,expression:"showTriggerDate"}]},[r("el-form-item",{staticClass:"required",attrs:{label:"Date",prop:"triggerDateForm",rules:[{required:e.showTriggerDate,message:"please choose the start date",trigger:"blur"}]}},[r("el-date-picker",{staticStyle:{width:"190px"},attrs:{type:"date",placeholder:"Choose date",format:"yyyy-MM-dd","value-format":"yyyy-MM-dd"},model:{value:e.addForm.triggerDateForm,callback:function(t){e.$set(e.addForm,"triggerDateForm",t)},expression:"addForm.triggerDateForm"}})],1)],1)])],1),e._l(e.addForm.customizePara.monitorParam,(function(t,a){return r("div",{key:t.key},[r("el-form-item",{staticClass:"required",attrs:{label:"Monitor Type "+(a+1),prop:"customizePara.monitorParam."+a+".type",rules:[{required:e.showCustomizeForm,message:"please choose the monitor type",trigger:"change"}]}},[r("el-form-item",[r("el-select",{attrs:{placeholder:"Please choice"},model:{value:t.type,callback:function(r){e.$set(t,"type",r)},expression:"item.type"}},e._l(e.monitorType.slice(0,-1),(function(e){return r("el-option",{attrs:{label:e[1],value:e[0]}})})),1),r("el-button",{staticStyle:{"margin-left":"20px"},attrs:{type:"info"},on:{click:function(r){return e.deleteCusMonitor(t)}}},[e._v("Delete")])],1)],1),r("el-form-item",{attrs:{label:"Period"}},[r("el-col",{attrs:{span:9}},[r("el-form-item",{attrs:{prop:"customizePara.monitorParam."+a+".period"}},[r("el-input",{staticClass:"shortInputForm",model:{value:t.period,callback:function(r){e.$set(t,"period",r)},expression:"item.period"}})],1)],1),r("el-col",{attrs:{span:13}},[r("el-form-item",{staticClass:"required",attrs:{label:"Total Times",prop:"customizePara.monitorParam."+a+".times",rules:[{required:e.showCustomizeForm,message:"please enter total times",trigger:"blur"},{validator:e.onlyNum}]}},[r("el-input",{staticClass:"shortInputForm",model:{value:t.times,callback:function(r){e.$set(t,"times",r)},expression:"item.times"}})],1)],1)],1)],1)})),r("el-form-item",[r("el-button",{attrs:{type:"primary"},on:{click:e.addCusMonitor}},[e._v("add Monitor")])],1)],2),r("div",{directives:[{name:"show",rawName:"v-show",value:!e.showCustomizeForm,expression:"!showCustomizeForm"}]},[r("el-form-item",{attrs:{label:"Period"}},[r("el-col",{attrs:{span:9}},[r("el-form-item",{attrs:{prop:"period"}},[r("el-input",{staticClass:"shortInputForm",model:{value:e.addForm.period,callback:function(t){e.$set(e.addForm,"period",t)},expression:"addForm.period"}})],1)],1),r("el-col",{attrs:{span:13}},[r("el-form-item",{staticClass:"required",attrs:{label:"Total Times",prop:"total_times",rules:[{required:!this.showCustomizeForm,message:"please enter total times",trigger:"blur"},{validator:e.onlyNum}]}},[r("el-input",{staticClass:"shortInputForm",model:{value:e.addForm.total_times,callback:function(t){e.$set(e.addForm,"total_times",t)},expression:"addForm.total_times"}})],1)],1)],1)],1),r("el-form-item",{attrs:{label:"Applied IPS",prop:"appliedIPS"}},[r("el-transfer",{attrs:{titles:["Unapplied","Applied"],data:e.IPSdata},model:{value:e.addForm.appliedIPS,callback:function(t){e.$set(e.addForm,"appliedIPS",t)},expression:"addForm.appliedIPS"}})],1)],1)],1),r("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{on:{click:function(t){e.dialogVisible=!1}}},[e._v("Cancel")]),r("el-button",{attrs:{type:"primary"},on:{click:e.addFTSI}},[e._v("Submit")])],1)])},i=[],o=(r("c975"),r("a434"),r("96cf"),r("1da1")),s={name:"addFTSI",data:function(){var e=function(e){for(var t=[],r=1;r<=15;r++)t.push({key:600100+r,label:"".concat(600100+r)});return t},t=function(e,t,r){var a=/^[0-9_]*$/;a.test(t)?r():r(new Error("The format of the input is illegal"))},r=function(e,t,r){var a=/^[A-Z]{1}$/;a.test(t)?r():r(new Error("The format of the Rev. is illegal"))};return{IPSdata:e(),dialogVisible:!1,activeDisabled:!1,pendingFlag:!1,monitorType:[],triggerType:[],showCustomizeForm:!1,showTriggerFTSI:!1,showTriggerDate:!1,addForm:{triggerDateForm:"",ftsi_num:"",rev:"",issueDate:"",ftsi_title:"",statement:"",dep_type:"",period:"",total_times:"",appliedIPS:[],customizePara:{trigger:{type:"NA",parameter:""},monitorParam:[{type:"",period:"",times:""}]}},addFormRules:{ftsi_num:[{required:!0,message:"please enter the FTSI number",trigger:"blur"},{validator:t,trigger:"blur"},{validator:this.validateFTSIexist,trigger:"blur"}],rev:[{required:!0,message:"please enter the Revision",trigger:"blur"},{validator:r,trigger:"blur"}],dep_type:[{required:!0,message:"please choose the monitor type",trigger:"change"}],appliedIPS:[{required:!0,message:"At least one IPS must be chosen",trigger:"change"}]}}},methods:{init:function(){this.getTypeFTSI()},initForPending:function(e){this.addForm.pending_id=e.id,this.addForm.ftsi_num=e.ftsi_no,this.addForm.rev=e.revision,this.addForm.ftsi_title=e.ftsi_title,this.addForm.statement=e.statement,this.addForm.issueDate=e.issue_date,this.addForm.appliedIPS=e.impact_ips,this.getTypeFTSI(),this.pendingFlag=!0},onlyNum:function(e,t,r){var a=/^[0-9_-]*$/;a.test(t)?r():r(new Error("The format of the input is illegal"))},validateFTSIexist:function(e,t,r){var a=this;return Object(o["a"])(regeneratorRuntime.mark((function e(){var i,o;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(t){e.next=2;break}return e.abrupt("return",r());case 2:return e.next=4,a.$http.get("ftsiMgr/FTSInumExistCheck/",{params:{ftsi_num:a.addForm.ftsi_num}});case 4:i=e.sent,o=i.data,200!==o.meta.status?r(new Error(o.meta.msg)):r();case 7:case"end":return e.stop()}}),e)})))()},addDialogClose:function(){this.$refs.addFormRef.resetFields(),this.showCustomizeForm=!1,this.showTriggerFTSI=!1,this.showTriggerDate=!1},getTypeFTSI:function(){var e=this;return Object(o["a"])(regeneratorRuntime.mark((function t(){var r,a;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.$http.get("ftsiMgr/paraforAddFTSI/");case 2:r=t.sent,a=r.data,200!==a.meta.status&&e.$message.error("failed to get the type list"),e.monitorType=a.data.monitorType,e.triggerType=a.data.triggerType,e.dialogVisible=!0;case 8:case"end":return t.stop()}}),t)})))()},monitorTypeCheck:function(){if("CUS"===this.addForm.dep_type)return this.addForm.total_times=1,this.addForm.period="",this.showCustomizeForm=!0;this.showCustomizeForm=!1,this.showTriggerFTSI=!1,this.showTriggerDate=!1},addCusMonitor:function(){if(this.addForm.customizePara.monitorParam.length>2)return this.$message.error("The amount must be no more than 3!");this.addForm.customizePara.monitorParam.push({type:"",period:"",times:""})},deleteCusMonitor:function(e,t){t=this.addForm.customizePara.monitorParam.indexOf(e);-1!==t&&this.addForm.customizePara.monitorParam.splice(t,1)},addFTSI:function(){var e=this;this.$refs.addFormRef.validate(function(){var t=Object(o["a"])(regeneratorRuntime.mark((function t(r){var a,i,o,s;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:if(r){t.next=2;break}return t.abrupt("return");case 2:return!0===e.showTriggerDate&&(e.addForm.customizePara.trigger.parameter=e.addForm.triggerDateForm),t.next=5,e.$http.post("ftsiMgr/addFTSI/",e.addForm);case 5:if(a=t.sent,i=a.data,201===i.meta.status){t.next=9;break}return t.abrupt("return",e.$message.error(i.meta.msg));case 9:if(!0!==e.pendingFlag){t.next=16;break}return t.next=12,e.$http.put("ftsiMgr/PendingClose/",e.addForm);case 12:o=t.sent,s=o.data,200!==s.meta.status&&e.$message.error(s.meta.msg),e.$message.success(s.meta.msg);case 16:e.dialogVisible=!1,e.$emit("updateList");case 18:case"end":return t.stop()}}),t)})));return function(e){return t.apply(this,arguments)}}())},paraShowControl:function(){this.addForm.customizePara.trigger.parameter="","NA"===this.addForm.customizePara.trigger.type?(this.showTriggerFTSI=!1,this.showTriggerDate=!1):"TFTSI"===this.addForm.customizePara.trigger.type?(this.showTriggerFTSI=!0,this.showTriggerDate=!1):(this.showTriggerFTSI=!1,this.showTriggerDate=!0)}}},n=s,l=(r("dffa"),r("2877")),d=Object(l["a"])(n,a,i,!1,null,"489d0800",null);t["default"]=d.exports},"1dde":function(e,t,r){var a=r("d039"),i=r("b622"),o=r("2d00"),s=i("species");e.exports=function(e){return o>=51||!a((function(){var t=[],r=t.constructor={};return r[s]=function(){return{foo:1}},1!==t[e](Boolean).foo}))}},"65f0":function(e,t,r){var a=r("861d"),i=r("e8b5"),o=r("b622"),s=o("species");e.exports=function(e,t){var r;return i(e)&&(r=e.constructor,"function"!=typeof r||r!==Array&&!i(r.prototype)?a(r)&&(r=r[s],null===r&&(r=void 0)):r=void 0),new(void 0===r?Array:r)(0===t?0:t)}},8418:function(e,t,r){"use strict";var a=r("c04e"),i=r("9bf2"),o=r("5c6c");e.exports=function(e,t,r){var s=a(t);s in e?i.f(e,s,o(0,r)):e[s]=r}},a434:function(e,t,r){"use strict";var a=r("23e7"),i=r("23cb"),o=r("a691"),s=r("50c4"),n=r("7b0b"),l=r("65f0"),d=r("8418"),m=r("1dde"),u=r("ae40"),c=m("splice"),p=u("splice",{ACCESSORS:!0,0:0,1:2}),g=Math.max,f=Math.min,h=9007199254740991,F="Maximum allowed length exceeded";a({target:"Array",proto:!0,forced:!c||!p},{splice:function(e,t){var r,a,m,u,c,p,v=n(this),b=s(v.length),y=i(e,b),T=arguments.length;if(0===T?r=a=0:1===T?(r=0,a=b-y):(r=T-2,a=f(g(o(t),0),b-y)),b+r-a>h)throw TypeError(F);for(m=l(v,a),u=0;u<a;u++)c=y+u,c in v&&d(m,u,v[c]);if(m.length=a,r<a){for(u=y;u<b-a;u++)c=u+a,p=u+r,c in v?v[p]=v[c]:delete v[p];for(u=b;u>b-a+r;u--)delete v[u-1]}else if(r>a)for(u=b-a;u>y;u--)c=u+a-1,p=u+r-1,c in v?v[p]=v[c]:delete v[p];for(u=0;u<r;u++)v[u+y]=arguments[u+2];return v.length=b-a+r,m}})},a640:function(e,t,r){"use strict";var a=r("d039");e.exports=function(e,t){var r=[][e];return!!r&&a((function(){r.call(null,t||function(){throw 1},1)}))}},ae40:function(e,t,r){var a=r("83ab"),i=r("d039"),o=r("5135"),s=Object.defineProperty,n={},l=function(e){throw e};e.exports=function(e,t){if(o(n,e))return n[e];t||(t={});var r=[][e],d=!!o(t,"ACCESSORS")&&t.ACCESSORS,m=o(t,0)?t[0]:l,u=o(t,1)?t[1]:void 0;return n[e]=!!r&&!i((function(){if(d&&!a)return!0;var e={length:-1};d?s(e,1,{enumerable:!0,get:l}):e[1]=1,r.call(e,m,u)}))}},c975:function(e,t,r){"use strict";var a=r("23e7"),i=r("4d64").indexOf,o=r("a640"),s=r("ae40"),n=[].indexOf,l=!!n&&1/[1].indexOf(1,-0)<0,d=o("indexOf"),m=s("indexOf",{ACCESSORS:!0,1:0});a({target:"Array",proto:!0,forced:l||!d||!m},{indexOf:function(e){return l?n.apply(this,arguments)||0:i(this,e,arguments.length>1?arguments[1]:void 0)}})},dffa:function(e,t,r){"use strict";r("e4c5")},e4c5:function(e,t,r){},e8b5:function(e,t,r){var a=r("c6b6");e.exports=Array.isArray||function(e){return"Array"==a(e)}}}]);
//# sourceMappingURL=chunk-091ca364.30f48c48.js.map
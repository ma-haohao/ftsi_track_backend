(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0c84d0"],{"53fb":function(t,e,s){"use strict";s.r(e);var i=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("el-dialog",{attrs:{title:"Results for the Predicted flight parameters",visible:t.dialogVisible,width:"800px"},on:{"update:visible":function(e){t.dialogVisible=e}}},[s("span",{directives:[{name:"show",rawName:"v-show",value:t.showOnWingPredict,expression:"showOnWingPredict"}]},[s("div",[s("h3",[t._v("LHE: "+t._s(t.results.leftIPS.engine))]),s("el-table",{staticStyle:{"font-size":"13px"},attrs:{data:t.results.ftsiForLeft,border:"",stripe:"","header-cell-style":{backgroundColor:"#6BA4FD",color:"#ffffff"}}},[s("el-table-column",{attrs:{label:"FTSI Num.",prop:"ftsi_info.ftsi_num,ftsi_info.rev",width:"110"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.ftsi_info.ftsi_num)+" Rev. "+t._s(e.row.ftsi_info.rev)+" ")]}}])}),s("el-table-column",{attrs:{label:"FTSI Title",prop:"ftsi_info.ftsi_title"}}),s("el-table-column",{attrs:{label:"Comments",prop:"content"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.content)+" left. ")]}}])})],1)],1),s("div",[s("h3",[t._v("RHE: "+t._s(t.results.rightIPS.engine))]),s("el-table",{staticStyle:{"font-size":"13px"},attrs:{data:t.results.ftsiForRight,border:"",stripe:"","header-cell-style":{backgroundColor:"#6BA4FD",color:"#ffffff"}}},[s("el-table-column",{attrs:{label:"FTSI Num.",prop:"ftsi_info.ftsi_num,ftsi_info.rev",width:"110"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.ftsi_info.ftsi_num)+" Rev. "+t._s(e.row.ftsi_info.rev)+" ")]}}])}),s("el-table-column",{attrs:{label:"FTSI Title",prop:"ftsi_info.ftsi_title"}}),s("el-table-column",{attrs:{label:"Comments",prop:"content"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.content)+" left. ")]}}])})],1)],1)]),s("span",{directives:[{name:"show",rawName:"v-show",value:t.showOffWingPredict,expression:"showOffWingPredict"}]},[s("div",[s("h3",[t._v("Off Wing IPS: "+t._s(t.results.leftIPS.engine))]),s("el-table",{staticStyle:{"font-size":"13px"},attrs:{data:t.results.ftsiForLeft,border:"",stripe:"","header-cell-style":{backgroundColor:"#6BA4FD",color:"#ffffff"}}},[s("el-table-column",{attrs:{label:"FTSI Num.",prop:"ftsi_info.ftsi_num,ftsi_info.rev",width:"110"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.ftsi_info.ftsi_num)+" Rev. "+t._s(e.row.ftsi_info.rev)+" ")]}}])}),s("el-table-column",{attrs:{label:"FTSI Title",prop:"ftsi_info.ftsi_title"}}),s("el-table-column",{attrs:{label:"Comments",prop:"content"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.content)+" left. ")]}}])})],1)],1)]),s("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[s("el-button",{on:{click:function(e){t.dialogVisible=!1}}},[t._v("close")])],1)])},o=[],l={name:"predictResultDisplay",data:function(){return{dialogVisible:!1,showOnWingPredict:!0,showOffWingPredict:!1,results:{leftIPS:{},rightIPS:{}}}},methods:{init:function(t){this.results=t,this.showOnWingPredict="NA"!==this.results.rightIPS.engine,this.showOffWingPredict=!this.showOnWingPredict,this.dialogVisible=!0,console.log(this.results)}}},n=l,r=s("2877"),f=Object(r["a"])(n,i,o,!1,null,"5e0ee92b",null);e["default"]=f.exports}}]);
//# sourceMappingURL=chunk-2d0c84d0.ae5cce84.js.map
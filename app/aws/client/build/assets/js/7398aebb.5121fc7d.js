"use strict";(self.webpackChunkclient_app=self.webpackChunkclient_app||[]).push([[781],{9801:(e,t,a)=>{a.r(t),a.d(t,{default:()=>o});var s=a(7294),n=a(2807),r=a(9669),l=a.n(r),c=a(6010),h=a(9547),m=a(7729),u=a(9960);class i extends s.Component{constructor(e){super(e)}render(){return 200==this.props.data.status?s.createElement(s.Fragment,null,s.createElement("h3",{className:m.Z.alert},"\u0110\u01b0\u1eddng d\u1eabn r\xfat g\u1ecdn:",s.createElement(u.Z,{href:this.props.data.message}," ",this.props.data.message))):s.createElement(s.Fragment,null,s.createElement("h1",{className:m.Z.status},this.props.data.status),s.createElement("h3",{className:m.Z.alert},this.props.data.message))}}class o extends s.Component{constructor(e){super(e),this.state={url:"",data:""}}handleChange(e){this.setState({url:e.target.value})}async handleSubmit(e){e.preventDefault();try{const e=await l().post("https://api.builetuananh.name.vn/dev",{data:{url:this.state.url}});this.setState({data:e.data})}catch(t){this.setState({data:t.response.data})}}render(){return s.createElement(n.Z,{title:"URL Shortener",description:"C\xf4ng c\u1ee5 r\xfat g\u1ecdn \u0111\u1ecba ch\u1ec9 URL"},s.createElement("header",{className:(0,c.Z)("hero hero--primary",h.Z.heroBanner)},s.createElement("div",{className:"container"},s.createElement("h1",{className:"hero__title"},"URL Shortener"),s.createElement("p",{className:"hero__subtitle"},"C\xf4ng c\u1ee5 r\xfat g\u1ecdn \u0111\u1ecba ch\u1ec9 URL"),s.createElement("form",{onSubmit:this.handleSubmit.bind(this)},s.createElement("label",null,s.createElement("input",{className:m.Z.url,type:"text",placeholder:"Nh\u1eadp \u0111\u1ecba ch\u1ec9 c\u1ea7n r\xfat g\u1ecdn (v\xed d\u1ee5 https://google.com)",name:"url",value:this.state.url,onChange:this.handleChange.bind(this),required:!0})),s.createElement("div",{className:h.Z.buttons},s.createElement("input",{className:"button button--secondary button--lg",type:"submit",value:"\ud83d\udd0d R\xfat g\u1ecdn"}))))),s.createElement("main",null,s.createElement("div",{className:"container"},s.createElement(i,{data:this.state.data,url:this.state.url}))))}}}}]);
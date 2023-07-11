import React, { Component } from "react";
import custom from "../../css/YoutubeFeatures.module.css";
import Link from "@docusaurus/Link";

export default class URLFeatures extends Component<{ url: string, data: any }, {}>  {
    constructor(props) {
        super(props);
    }

    render() {
        if (this.props.data.status == 200)
            return (
                <>
                    <h3 className={custom.alert}>Đường dẫn rút gọn:
                        <Link href={this.props.data.message}> {this.props.data.message}</Link></h3>
                </>
            );
        else
            return (
                <>

                    <h1 className={custom.status}>{this.props.data.status}</h1>
                    <h3 className={custom.alert}>{this.props.data.message}</h3>
                </>
            );
    }
}
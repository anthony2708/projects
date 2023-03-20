import React, { Component } from "react";
import custom from "../css/YoutubeFeatures.module.css";
import Link from "@docusaurus/Link";

export default class YoutubeFeatures extends Component<{ data: any, url: string }, {}> {
    constructor(props) {
        super(props);
    }

    render() {
        if (this.props.data.info != undefined && this.props.url.includes("youtube.com/watch?v="))
            return (
                <>
                    <h3 className={custom.alert}>Tìm thấy video: {this.props.data.title}</h3>
                    <div className={custom.iframe_container}>
                        <iframe className={custom.center} src={this.props.data.url}></iframe>
                    </div>
                    <div>
                        <table className={custom.table_center}>
                            <thead>
                                <tr>
                                    <th>Phiên bản</th>
                                    <th>Chất lượng hình ảnh</th>
                                    <th>Có/Không có tiếng?</th>
                                    <th>Đường dẫn</th>
                                </tr>
                            </thead>
                            <tbody>
                                {this.props.data.info.map((item) => {
                                    return (
                                        <tr key={item.url}>
                                            <td>{item.mimeType.split(";")[0]}</td>
                                            <td>{item.hasVideo ? item.height + "p" : ""}</td>
                                            <td>{item.hasAudio ? "✔" : "❌"}</td>
                                            <td><Link className="button button--primary button--md"
                                                href={item.url}>🔽 Tải xuống</Link></td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
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
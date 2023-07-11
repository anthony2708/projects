import React, { Component } from "react";
import Layout from "@theme/Layout";
import axios from "axios";
import clsx from "clsx";
import styles from "../css/index.module.css";
import custom from "../css/YoutubeFeatures.module.css";
import YoutubeFeatures from "../components/YoutubeFeatures";

export default class Youtube extends Component<{}, { url: string, data: any }> {
    constructor(props: {} | Readonly<{}>) {
        super(props);
        this.state = { url: "", data: "" };
    }

    handleChange(event: { target: { value: any } }) {
        this.setState({ url: event.target.value });
    }

    async handleSubmit(event: { preventDefault: () => void }) {
        event.preventDefault();
        try {
            const res = await axios.post('https://api.builetuananh.name.vn/api/getVideo',
                { data: { url: this.state.url } });
            this.setState({ data: res.data });
        } catch (error) {
            this.setState({ data: error.response.data });
        }
    }

    render() {
        return (
            <Layout title={`Youtube Downloader`} description="Công cụ tải xuống video từ Youtube">
                {/* Header */}
                <header className={clsx("hero hero--primary", styles.heroBanner)}>
                    <div className="container">
                        <h1 className="hero__title">Youtube Downloader</h1>
                        <p className="hero__subtitle">Công cụ tải xuống video từ Youtube</p>
                        <form onSubmit={this.handleSubmit.bind(this)}>
                            <label>
                                <input className={custom.url} type="text"
                                    placeholder="Nhập địa chỉ video (ví dụ https://youtube.com)"
                                    name="url" value={this.state.url}
                                    onChange={this.handleChange.bind(this)} required />
                            </label>
                            <div className={styles.buttons}>
                                <input className="button button--secondary button--lg" type="submit"
                                    value="🔍 Tìm kiếm" />
                            </div>
                        </form>
                    </div>
                </header>
                {/* End of Header */}
                <main>
                    <div className="container">
                        <YoutubeFeatures data={this.state.data} url={this.state.url} />
                    </div>
                </main>
            </Layout >
        );
    }
}
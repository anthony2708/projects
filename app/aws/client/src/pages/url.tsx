import React, { Component } from "react";
import Layout from "@theme/Layout";
import axios from "axios";
import clsx from "clsx";
import styles from "../css/index.module.css";
import custom from "../css/YoutubeFeatures.module.css";
import URLFeatures from "../components/URLFeatures";

export default class URL extends Component<{}, { url: string, data: any }> {
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
            const res = await axios.post('https://api.builetuananh.name.vn/dev',
                { data: { url: this.state.url } });
            this.setState({ data: res.data });
        } catch (error) {
            this.setState({ data: error.response.data });
        }
    }

    render() {
        return (
            <Layout title={`URL Shortener`} description="Công cụ rút gọn địa chỉ URL">
                {/* Header */}
                <header className={clsx("hero hero--primary", styles.heroBanner)}>
                    <div className="container">
                        <h1 className="hero__title">URL Shortener</h1>
                        <p className="hero__subtitle">Công cụ rút gọn địa chỉ URL</p>
                        <form onSubmit={this.handleSubmit.bind(this)}>
                            <label>
                                <input className={custom.url} type="text"
                                    placeholder="Nhập địa chỉ cần rút gọn (ví dụ https://google.com)"
                                    name="url" value={this.state.url}
                                    onChange={this.handleChange.bind(this)} required />
                            </label>
                            <div className={styles.buttons}>
                                <input className="button button--secondary button--lg" type="submit"
                                    value="🔍 Rút gọn" />
                            </div>
                        </form>
                    </div>
                </header>
                {/* End of Header */}
                <main>
                    <div className="container">
                        <URLFeatures data={this.state.data} url={this.state.url} />
                    </div>
                </main>
            </Layout >
        );
    }
}
import React, { useEffect, useState } from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from '../css/index.module.css';
import HomepageFeatures from '../components/HomepageFeatures';

function HomepageHeader() {
  const [dateState, setDateState] = useState(new Date());
  useEffect(() => {
    const timer = setInterval(() => { setDateState(new Date()); }, 1000);
    return () => { clearInterval(timer); };
  });
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">
          {
            dateState.toLocaleTimeString('vi-VN', {
              hour12: false,
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit',
            })
          }
        </h1>
        <p className="hero__subtitle">
          {
            dateState.toLocaleDateString('vi-VN', {
              weekday: 'long',
              day: '2-digit',
              month: '2-digit',
              year: 'numeric',
            })
          }
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Giới thiệu - 5 phút ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  return (
    <Layout title={`Trang chủ`} description="Anthony Bùi Lê Tuấn Anh">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}

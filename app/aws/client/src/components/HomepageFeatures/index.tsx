import React from 'react';
import clsx from 'clsx';
import styles from '../../css/styles.module.css';
import Link from '@docusaurus/Link';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
  link: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Youtube Downloader',
    Svg: require('@site/public/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Dịch vụ cho phép người dùng tải xuống các video từ Youtube một cách miễn phí
        và không vi phạm bản quyền.
      </>
    ),
    link: '/youtube'
  },
  {
    title: 'URL Shortener',
    Svg: require('@site/public/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Cổng dịch vụ cho phép thực hiện việc rút gọn và truy cập các đường dẫn trang web
        khác nhau, giúp tiết kiệm thời gian, chi phí và công sức thực hiện.
      </>
    ),
    link: '/url'
  },
  // {
  //   title: 'Powered by React',
  //   Svg: require('@site/public/img/undraw_docusaurus_react.svg').default,
  //   description: (
  //     <>
  //       Extend or customize your website layout by reusing React. Docusaurus can
  //       be extended while reusing the same header and footer.
  //     </>
  //   ),
  // },
];

function Feature({ title, Svg, description, link }: FeatureItem) {
  return (
    <div className={clsx('col col--6')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
        <Link
          className="button button--primary button--md"
          to={link}>
          🖱 Truy cập
        </Link>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

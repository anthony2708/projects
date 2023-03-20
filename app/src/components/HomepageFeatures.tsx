import useBaseUrl from '@docusaurus/useBaseUrl';
import React from 'react';
import clsx from 'clsx';
import styles from '../css/HomepageFeatures.module.css';

type FeatureItem = {
  title: string;
  image: string;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: "CN Mạng Máy tính & Truyền thông",
    image: "/img/favicon/logo_khtn_remake_1.svg",
    description: (
      <>
        Khoa Công nghệ thông tin, Trường Đại học Khoa học Tự nhiên, Đại học Quốc
        gia Thành phố Hồ Chí Minh (VNUHCM_US, 2019 - 2023).
      </>
    ),
  },
  {
    title: "❤ Hữu xạ tự nhiên hương ❤",
    image: "/img/docusaurus/undraw_docusaurus_tree.svg",
    description: (
      <>
        Một người lạc quan, chăm chỉ và có trách nhiệm. Đam mê lập trình Web
        và Mạng máy tính. Thích nghe nhạc, chơi đá bóng và xem TV.
      </>
    ),
  },
  {
    title: "Chuyên tiếng Anh - Khóa 23",
    image: "img/favicon/logo_HLK.svg",
    description: (
      <>
        Trường Trung học phổ thông Chuyên Hoàng Lê Kha - Tây Ninh (2016 - 2019).
        Nhận học bổng khuyến khích trong cả 3 năm học.
      </>
    ),
  },
];

function Feature({ title, image, description }: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img
          className={styles.featureSvg}
          alt={title}
          src={useBaseUrl(image)}
        />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
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

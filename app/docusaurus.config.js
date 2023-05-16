// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Anthony Bùi Lê Tuấn Anh",
  tagline: "❤ Đồng thanh tương ứng, đồng khí tương cầu ❤",
  url: "https://www.builetuananh.name.vn",
  baseUrl: "/",
  staticDirectories: ["public"],
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon/favicon.png",
  organizationName: "anthony2708", // Usually your GitHub org/user name.
  projectName: "anthony2708", // Usually your repo name.
  deploymentBranch: "gh-pages",
  trailingSlash: false,
  i18n: {
    defaultLocale: "vi",
    locales: ["vi", "en"],
    localeConfigs: {
      vi: {
        htmlLang: "vi-VN",
      },
    },
  },
  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
        },
        blog: {
          showReadingTime: true,
          routeBasePath: "blog",
          path: "./blog/tech",
          authorsMapPath: "../authors.yml",
        },
        theme: {
          customCss: [require.resolve("./src/css/custom.css")],
        },
      }),
    ],
  ],

  plugins: [
    [
      "@docusaurus/plugin-content-blog",
      {
        id: "second-blog",
        routeBasePath: "collab",
        path: "./blog/collaboration",
        authorsMapPath: "../authors.yml",
      },
    ],
    [
      "@docusaurus/plugin-content-blog",
      {
        id: "third-blog",
        routeBasePath: "hlk",
        path: "./blog/HLK_MyYouth",
        authorsMapPath: "../authors.yml",
      },
    ],
    [
      "@docusaurus/plugin-content-blog",
      {
        id: "fourth-blog",
        routeBasePath: "spring",
        path: "./blog/SpringStories",
        authorsMapPath: "../authors.yml",
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        hideOnScroll: true,
        title: "Anthony Bùi Lê Tuấn Anh",
        logo: {
          alt: "Logo",
          src: "img/favicon/ET_Logo.png",
        },
        items: [
          {
            label: "Giới thiệu",
            type: "doc",
            docId: "intro",
            position: "left",
          },
          {
            type: "dropdown",
            label: "Blog cá nhân",
            position: "left",
            items: [
              {
                label: "Tech Blog",
                to: "/blog",
              },
              {
                label: "The Collab Team",
                to: "/collab",
              },
              {
                label: "Hồi ký Hoàng chuyên",
                to: "/hlk",
              },
              {
                label: "Câu chuyện mùa xuân",
                to: "/spring",
              },
            ],
          },
          {
            label: "Cổng dịch vụ",
            position: "left",
            href: "https://services.builetuananh.name.vn",
          },
          {
            href: "https://github.com/anthony2708",
            position: "right",
            className: "header-github-link", // custom logo in custom.css
            "aria-label": "GitHub",
          },
          {
            type: "localeDropdown",
            position: "right",
          },
        ],
      },
      announcementBar: {
        id: "announcement-bar",
        content:
          "📧 <b>Email</b>: <a target='_blank' rel='noopener noreferrer' href='mailto:builetuananh2708@gmail.com'>builetuananh2708@gmail.com</a> | 📞 <b>Tel</b>: <a target='_blank' rel='noopener noreferrer' href='tel:+84937826135'>(+84/0) 937826135</a>",
        backgroundColor: "#a4e4dc",
        textColor: "#222",
        isCloseable: false,
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Trang chủ",
            items: [
              {
                label: "Giới thiệu cá nhân",
                to: "/docs/intro",
              },
              {
                label: "Thông tin liên hệ",
                to: "/docs/contact",
              },
              {
                label: "Tài liệu tham khảo",
                to: "/docs/resources",
              },
              {
                label: "Cổng dịch vụ",
                href: "https://services.builetuananh.name.vn",
              },
            ],
          },
          {
            title: "Blog cá nhân",
            items: [
              {
                label: "Tech Blog",
                to: "/blog",
              },
              {
                label: "The Collab Team",
                to: "/collab",
              },
              {
                label: "Hồi ký Hoàng chuyên",
                to: "/hlk",
              },
              {
                label: "Câu chuyện mùa xuân",
                to: "/spring",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Anthony Bùi Lê Tuấn Anh. Built with ❤ & <a href="https://docusaurus.io" target="_blank" rel="noopener noreferrer">Docusaurus</a>.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ["docker"],
      },
    }),
};

module.exports = config;
